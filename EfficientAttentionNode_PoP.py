import torch
import torch.nn as nn
import torch.nn.functional as F
import logging
from typing import Tuple, Dict, Optional, Any, List
from contextlib import contextmanager
import math

class EfficientAttentionNode:
    """
    A custom node for ComfyUI that implements an efficient attention mechanism.
    This node can be used to modify the attention behavior of existing models.
    """

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        """
        Defines the input types for the node in the ComfyUI interface.
        
        Returns:
            A dictionary specifying the input types and their properties.
        """
        return {
            "required": {
                "model": ("MODEL",),
                "strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 2.0, "step": 0.01}),
                "attention_variant": (["default", "linear"], {"default": "default"}),
                "use_dropout": ("BOOLEAN", {"default": False}),
                "dropout_rate": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 0.5, "step": 0.01}),
                "use_layer_norm": ("BOOLEAN", {"default": False}),
                "init_method": (["none", "xavier", "he", "orthogonal"], {"default": "none"}),
                "scaling_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
                "use_warmup": ("BOOLEAN", {"default": False}),
                "warmup_steps": ("INT", {"default": 0, "min": 0, "max": 500, "step": 1}),
                "warmup_type": (["linear_up", "linear_down", "cosine_up", "cosine_down"], {"default": "linear_up"}),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_efficient_attention"
    CATEGORY = "PoP/attention"

    def __init__(self):
        """
        Initialize the EfficientAttentionNode with default values and placeholders for layers.
        """
        self.to_q: Optional[nn.Linear] = None
        self.to_k: Optional[nn.Linear] = None
        self.to_v: Optional[nn.Linear] = None
        self.strength: float = 0.0
        self.init_method: str = "none"
        self.use_layer_norm: bool = False
        self.layer_norm: Optional[nn.LayerNorm] = None
        self.dropout: Optional[nn.Dropout] = None
        self.attention_variant: str = "default"
        self.scaling_factor: float = 1.0
        self.use_warmup: bool = False
        self.warmup_steps: int = 0
        self.warmup_type: str = "linear_up"
        self.current_step: int = 0

    @contextmanager
    def error_handling(self, method_name: str):
        """
        Context manager for consistent error handling across the class.
        
        Args:
            method_name (str): Name of the method where the error occurred.
        """
        try:
            yield
        except Exception as e:
            logging.error(f"Error in {method_name}: {str(e)}")
            raise

    def initialize_linear_layer(self, layer: nn.Linear):
        """
        Initialize the weights of a linear layer based on the chosen initialization method.
        
        Args:
            layer (nn.Linear): The linear layer to initialize.
        """
        with self.error_handling("initialize_linear_layer"):
            if self.init_method == "xavier":
                nn.init.xavier_uniform_(layer.weight)
            elif self.init_method == "he":
                nn.init.kaiming_uniform_(layer.weight, nonlinearity='relu')
            elif self.init_method == "orthogonal":
                # Convert to float32, initialize, then convert back
                orig_dtype = layer.weight.dtype
                layer.weight.data = layer.weight.to(torch.float32)
                nn.init.orthogonal_(layer.weight)
                layer.weight.data = layer.weight.to(orig_dtype)

    def default_attention(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Compute attention using the default scaled dot-product mechanism.
        
        Args:
            q, k, v (torch.Tensor): Query, Key, and Value tensors.
            mask (Optional[torch.Tensor]): Attention mask.
        
        Returns:
            torch.Tensor: Output of the attention mechanism.
        """
        scale = self.scaling_factor * (q.size(-1) ** -0.5)
        sim = torch.einsum('b i d, b j d -> b i j', q, k) * scale
        if mask is not None:
            sim = sim.masked_fill(mask == 0, -float('inf'))
        attn = sim.softmax(dim=-1)
        if self.dropout is not None:
            attn = self.dropout(attn)
        return torch.einsum('b i j, b j d -> b i d', attn, v)

    def linear_attention(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Compute attention using a linear attention variant.
        
        Args:
            q, k, v (torch.Tensor): Query, Key, and Value tensors.
            mask (Optional[torch.Tensor]): Attention mask.
        
        Returns:
            torch.Tensor: Output of the attention mechanism.
        """
        q = q.softmax(dim=-1)
        k = k.softmax(dim=-2)
        if mask is not None:
            k = k * mask.float().unsqueeze(1)
        context = torch.einsum('b j d, b j e -> b d e', k, v)
        return torch.einsum('b i d, b d e -> b i e', q, context)

    def efficient_attention(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, heads: int, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Main method for computing efficient attention.
        
        Args:
            q, k, v (torch.Tensor): Query, Key, and Value tensors.
            heads (int): Number of attention heads.
            mask (Optional[torch.Tensor]): Attention mask.
        
        Returns:
            torch.Tensor: Output of the attention mechanism.
        """
        with self.error_handling("efficient_attention"):
            # Ensure consistent dtype
            dtype = q.dtype
            q, k, v = q.to(dtype), k.to(dtype), v.to(dtype)
            
            # Get tensor dimensions
            b, seq_len_q, dim_q = q.shape
            _, seq_len_k, dim_k = k.shape
            is_self_attention = (q.shape == k.shape == v.shape)
            dim_head = dim_q // heads

            # Handle cross-attention case
            if not is_self_attention:
                if self.to_k is None or self.to_k.in_features != dim_k or self.to_k.out_features != dim_q:
                    self.to_k = nn.Linear(dim_k, dim_q, bias=False).to(device=q.device, dtype=dtype)
                    self.to_v = nn.Linear(dim_k, dim_q, bias=False).to(device=q.device, dtype=dtype)
                    self.initialize_linear_layer(self.to_k)
                    self.initialize_linear_layer(self.to_v)
                k = self.to_k(k)
                v = self.to_v(v)

            # Ensure consistent dimensions
            min_dim = min(q.shape[-1], k.shape[-1], v.shape[-1])
            q = q[..., :min_dim]
            k = k[..., :min_dim]
            v = v[..., :min_dim]

            # Reshape for multi-head attention
            q = q.view(b * heads, seq_len_q, dim_head)
            k = k.view(b * heads, seq_len_k, dim_head)
            v = v.view(b * heads, seq_len_k, dim_head)

            # Apply attention
            if self.attention_variant == "linear":
                out = self.linear_attention(q, k, v, mask)
            else:
                out = self.default_attention(q, k, v, mask)

            # Reshape output
            out = out.view(b, seq_len_q, dim_q)

            # Apply layer normalization if enabled
            if self.use_layer_norm:
                if self.layer_norm is None or self.layer_norm.normalized_shape != (dim_q,):
                    self.layer_norm = nn.LayerNorm(dim_q).to(device=out.device, dtype=dtype)
                out = self.layer_norm(out)

            return out

    def get_warmup_strength(self) -> float:
        """
        Calculate the current strength based on the warmup schedule.
        
        Returns:
            float: Current strength value.
        """
        if not self.use_warmup or self.warmup_steps == 0:
            return self.strength
        
        progress = self.current_step / self.warmup_steps
        
        if self.warmup_type == "linear_up":
            return progress * self.strength
        elif self.warmup_type == "linear_down":
            return (1 - progress) * self.strength
        elif self.warmup_type == "cosine_up":
            return self.strength * (1 - math.cos(progress * math.pi)) / 2
        elif self.warmup_type == "cosine_down":
            return self.strength * (1 + math.cos(progress * math.pi)) / 2
        else:
            raise ValueError(f"Unknown warmup type: {self.warmup_type}")

    def attention_patch(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, options: Dict[str, Any]) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Main method for applying the efficient attention mechanism.
        
        Args:
            q, k, v (torch.Tensor): Query, Key, and Value tensors.
            options (Dict[str, Any]): Additional options for attention computation.
        
        Returns:
            Tuple[torch.Tensor, torch.Tensor, torch.Tensor]: Modified q, k, v tensors.
        """
        with self.error_handling("attention_patch"):
            logging.debug(f"Attention patch called. use_warmup: {self.use_warmup}, warmup_steps: {self.warmup_steps}, current_step: {self.current_step}, strength: {self.strength}")

            if self.strength == 0:
                return q, k, v

            heads = options.get("n_heads")
            if heads is None:
                # ...
                raise ValueError("Number of heads (n_heads) must be specified in options")

            dtype = q.dtype
            q, k, v = q.to(dtype), k.to(dtype), v.to(dtype)

            efficient_output = self.efficient_attention(q, k, v, heads)
            current_strength = self.get_warmup_strength()

            logging.debug(f"Current strength: {current_strength}")

            result = q + current_strength * (efficient_output - q)
            self.step()

            return result, k, v

    def step(self):
        """
        Increment the current step for warmup calculations.
        """
        if self.use_warmup and self.current_step < self.warmup_steps:
            self.current_step += 1

    def apply_efficient_attention(self, model: Any, strength: float, attention_variant: str, 
                                  use_dropout: bool, dropout_rate: float, use_layer_norm: bool, 
                                  init_method: str, scaling_factor: float,
                                  use_warmup: bool, warmup_steps: int, warmup_type: str) -> Tuple[Any]:
        """
        Apply the efficient attention mechanism to the given model.
        
        Args:
            model (Any): The input model to modify.
            strength (float): Strength of the attention mechanism.
            attention_variant (str): Type of attention to use.
            use_dropout (bool): Whether to use dropout.
            dropout_rate (float): Dropout rate.
            use_layer_norm (bool): Whether to use layer normalization.
            init_method (str): Weight initialization method.
            scaling_factor (float): Scaling factor for attention computation.
            use_warmup (bool): Whether to use warmup.
            warmup_steps (int): Number of warmup steps.
            warmup_type (str): Type of warmup schedule.
        
        Returns:
            Tuple[Any]: Modified model.
        """
        with self.error_handling("apply_efficient_attention"):
            # Set instance variables
            self.strength = strength
            self.attention_variant = attention_variant
            self.use_layer_norm = use_layer_norm
            self.init_method = init_method
            self.scaling_factor = scaling_factor
            self.use_warmup = use_warmup
            self.warmup_steps = max(0, warmup_steps)  # Ensure non-negative
            self.warmup_type = warmup_type
            self.current_step = 0  # Reset current_step here

            logging.debug(f"Applying efficient attention. strength: {strength}, use_warmup: {use_warmup}, warmup_steps: {warmup_steps}, warmup_type: {warmup_type}")

            # Set up dropout
            if use_dropout and dropout_rate > 0:
                self.dropout = nn.Dropout(dropout_rate)
            else:
                self.dropout = None

            # If strength is 0, return the original model
            if strength == 0:
                return (model,)

            # Clone the model and apply the attention patch
            model_patcher = model.clone()
            if hasattr(model_patcher, 'set_model_attn1_patch') and hasattr(model_patcher, 'set_model_attn2_patch'):
                def wrapped_attention_patch(q, k, v, options):
                    dtype = q.dtype
                    q, k, v = q.to(dtype), k.to(dtype), v.to(dtype)
                    return self.attention_patch(q, k, v, options)

                model_patcher.set_model_attn1_patch(wrapped_attention_patch)
                model_patcher.set_model_attn2_patch(wrapped_attention_patch)
                return (model_patcher,)
            else:
                logging.error("model_patcher does not have required attention patch methods")
                return (model,)

# ComfyUI node registration
NODE_CLASS_MAPPINGS = {
    "EfficientAttention": EfficientAttentionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EfficientAttention": "Efficient Attention (PoP)"
}