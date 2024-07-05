from .AnyAspectRatio import NODE_CLASS_MAPPINGS as AnyAspectRatio_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as AnyAspectRatio_DISPLAY_NAME_MAPPINGS
from .LoraStackLoaders_PoP import NODE_CLASS_MAPPINGS as LoraStackLoaders_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoraStackLoaders_PoP_DISPLAY_NAME_MAPPINGS
from .AdaptiveCannyDetector_PoP import NODE_CLASS_MAPPINGS as AdaptiveCannyDetector_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as AdaptiveCannyDetector_PoP_DISPLAY_NAME_MAPPINGS
from .LoadImageResizer_PoP import NODE_CLASS_MAPPINGS as LoadImageResizer_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoadImageResizer_PoP_DISPLAY_NAME_MAPPINGS
from .Conditioning_PoP import NODE_CLASS_MAPPINGS as Conditioning_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as Conditioning_PoP_DISPLAY_NAME_MAPPINGS
from .VAEEncodeDecodeLoader_PoP import NODE_CLASS_MAPPINGS as VAEEncodeDecodeLoader_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as VAEEncodeDecodeLoader_PoP_DISPLAY_NAME_MAPPINGS 
from .EfficientAttentionNode_PoP import NODE_CLASS_MAPPINGS as EfficientAttention_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as EfficientAttention_PoP_DISPLAY_NAME_MAPPINGS
from .openAI_PoP import NODE_CLASS_MAPPINGS as openAI_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as openAI_PoP_DISPLAY_NAME_MAPPINGS

NODE_CLASS_MAPPINGS = {
    **AnyAspectRatio_MAPPINGS,
    **LoraStackLoaders_PoP_MAPPINGS,
    **AdaptiveCannyDetector_PoP_MAPPINGS,
    **LoadImageResizer_PoP_MAPPINGS,
    **Conditioning_PoP_MAPPINGS,
    **VAEEncodeDecodeLoader_PoP_MAPPINGS,
    **EfficientAttention_PoP_MAPPINGS,  
    **openAI_PoP_MAPPINGS
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **AnyAspectRatio_DISPLAY_NAME_MAPPINGS,
    **LoraStackLoaders_PoP_DISPLAY_NAME_MAPPINGS,
    **AdaptiveCannyDetector_PoP_DISPLAY_NAME_MAPPINGS,
    **LoadImageResizer_PoP_DISPLAY_NAME_MAPPINGS,
    **Conditioning_PoP_DISPLAY_NAME_MAPPINGS,
    **VAEEncodeDecodeLoader_PoP_DISPLAY_NAME_MAPPINGS,
    **EfficientAttention_PoP_DISPLAY_NAME_MAPPINGS,
    **openAI_PoP_DISPLAY_NAME_MAPPINGS,
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
