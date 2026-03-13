import math
import torch
import torch.nn.functional as F


# ---------------------------------------------------------------------------
# Window helpers
# ---------------------------------------------------------------------------

def _window_partition(x: torch.Tensor, window_size: int) -> torch.Tensor:
    """
    Partition a spatial feature map into non-overlapping windows.

    Args:
        x: Tensor of shape (B, H, W, C).
        window_size: Size of each square window.

    Returns:
        windows: Tensor of shape (num_windows * B, window_size, window_size, C).
    """
    B, H, W, C = x.shape
    x = x.view(B, H // window_size, window_size, W // window_size, window_size, C)
    windows = x.permute(0, 1, 3, 2, 4, 5).contiguous().view(-1, window_size, window_size, C)
    return windows


def _window_reverse(windows: torch.Tensor, window_size: int, H: int, W: int) -> torch.Tensor:
    """
    Reverse the window partition back into the full spatial feature map.

    Args:
        windows: Tensor of shape (num_windows * B, window_size, window_size, C).
        window_size: Size of each square window.
        H: Original spatial height.
        W: Original spatial width.

    Returns:
        x: Tensor of shape (B, H, W, C).
    """
    B = int(windows.shape[0] / (H * W / window_size / window_size))
    x = windows.view(B, H // window_size, W // window_size, window_size, window_size, -1)
    x = x.permute(0, 1, 3, 2, 4, 5).contiguous().view(B, H, W, -1)
    return x


def _infer_spatial_dims(seq_len: int, original_shape):
    """
    Infer (H, W) from the sequence length and the original input shape.

    ComfyUI passes ``original_shape`` as [B, C, H, W] in ``extra_options``.
    The actual feature-map resolution at different UNet levels is a
    power-of-two downsampling of the original latent spatial dimensions.

    Falls back to a square-root estimate when ``original_shape`` is absent.

    Returns:
        (h, w) if inference succeeds, (None, None) otherwise.
    """
    if original_shape is not None:
        orig_h, orig_w = int(original_shape[2]), int(original_shape[3])
        for factor in (1, 2, 4, 8):
            h = orig_h // factor
            w = orig_w // factor
            if h > 0 and w > 0 and h * w == seq_len:
                return h, w
    # Fallback: assume square feature map
    h = int(math.isqrt(seq_len))
    if h * h == seq_len:
        return h, h
    return None, None


def _windowed_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    h: int,
    w: int,
    window_size: int,
) -> torch.Tensor:
    """
    Compute window-based self-attention (MSW-MSA core).

    Attention is computed independently within each non-overlapping window,
    dramatically reducing memory and compute for high-resolution feature maps.

    Args:
        q, k, v: Tensors of shape (B, seq_len, C) where seq_len = h * w.
        h, w: Spatial height and width.
        window_size: Side length of each attention window.

    Returns:
        output: Tensor of shape (B, seq_len, C).
    """
    B, seq_len, C = q.shape
    ws = min(window_size, h, w)

    # Pad spatial dimensions to be multiples of window_size
    pad_h = (ws - h % ws) % ws
    pad_w = (ws - w % ws) % ws

    def to_spatial(t: torch.Tensor) -> torch.Tensor:
        return t.view(B, h, w, C)

    q_s, k_s, v_s = to_spatial(q), to_spatial(k), to_spatial(v)

    if pad_h > 0 or pad_w > 0:
        def pad_t(t: torch.Tensor) -> torch.Tensor:
            return F.pad(t.permute(0, 3, 1, 2), (0, pad_w, 0, pad_h)).permute(0, 2, 3, 1)
        q_s, k_s, v_s = pad_t(q_s), pad_t(k_s), pad_t(v_s)

    Hp, Wp = h + pad_h, w + pad_w
    win_area = ws * ws

    q_win = _window_partition(q_s, ws).view(-1, win_area, C)
    k_win = _window_partition(k_s, ws).view(-1, win_area, C)
    v_win = _window_partition(v_s, ws).view(-1, win_area, C)

    scale = C ** -0.5
    attn = torch.bmm(q_win * scale, k_win.transpose(1, 2))
    attn = torch.softmax(attn, dim=-1)
    out_win = torch.bmm(attn, v_win)

    out_win = out_win.view(-1, ws, ws, C)
    out = _window_reverse(out_win, ws, Hp, Wp)

    if pad_h > 0 or pad_w > 0:
        out = out[:, :h, :w, :].contiguous()

    return out.view(B, seq_len, C)


# ---------------------------------------------------------------------------
# Node definition
# ---------------------------------------------------------------------------

class HiDiffusionNode_PoP:
    """
    Applies HiDiffusion optimisation techniques to a diffusion model for
    higher-resolution image generation without additional training.

    Two complementary techniques are implemented:

    **MSW-MSA** — Multi-Scale Window Multi-Scale Attention
        Replaces the global self-attention in the UNet with efficient
        window-based attention.  Each spatial position only attends to
        neighbours inside its window, cutting memory and compute
        dramatically at high resolutions.  The windowed-attention output
        is blended with the original query via ``msw_strength`` before
        the standard ComfyUI attention pipeline continues, allowing a
        smooth transition between pure global and pure windowed attention.

    **RAU-Net** — Resolution-Aware U-Net
        Scales down the skip connections fed from the UNet encoder into
        the decoder output blocks.  At high resolutions the encoder
        features tend to introduce low-frequency spatial repetition into
        the decoder; reducing their magnitude forces the decoder to rely
        more on its own learned representations, yielding crisper
        high-res outputs.

    Reference: *HiDiffusion: Unlocking Higher-Resolution Creativity and
    Efficiency in Pretrained Diffusion Models* (Zhang et al., 2023).
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "apply_msw_msa": (
                    "BOOLEAN",
                    {"default": True, "tooltip": "Enable MSW-MSA windowed self-attention."},
                ),
                "msw_strength": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.01,
                        "tooltip": (
                            "Blend between original query (0.0) and windowed-attention "
                            "output (1.0) before the standard attention pass."
                        ),
                    },
                ),
                "window_size": (
                    "INT",
                    {
                        "default": 8,
                        "min": 2,
                        "max": 64,
                        "step": 2,
                        "tooltip": (
                            "Side length of each attention window. "
                            "Smaller windows are faster; larger windows capture more context."
                        ),
                    },
                ),
                "apply_rau_net": (
                    "BOOLEAN",
                    {"default": True, "tooltip": "Enable RAU-Net skip-connection scaling."},
                ),
                "rau_net_strength": (
                    "FLOAT",
                    {
                        "default": 0.5,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.01,
                        "tooltip": (
                            "How strongly to attenuate skip connections in the UNet "
                            "output blocks (0 = no change, 1 = skip connections zeroed)."
                        ),
                    },
                ),
                "rau_net_skip_threshold": (
                    "INT",
                    {
                        "default": 6,
                        "min": 0,
                        "max": 11,
                        "step": 1,
                        "tooltip": (
                            "Output-block index at which RAU-Net skip-connection "
                            "scaling begins.  Lower values affect more blocks."
                        ),
                    },
                ),
            }
        }

    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("model",)
    FUNCTION = "apply_hidiffusion"
    CATEGORY = "PoP/HiDiffusion"

    def apply_hidiffusion(
        self,
        model,
        apply_msw_msa: bool,
        msw_strength: float,
        window_size: int,
        apply_rau_net: bool,
        rau_net_strength: float,
        rau_net_skip_threshold: int,
    ):
        model = model.clone()

        # ── MSW-MSA ─────────────────────────────────────────────────────────
        if apply_msw_msa and msw_strength > 0.0:
            _ws = window_size
            _msw_s = msw_strength

            def msw_msa_attn1_patch(q, k, v, extra_options):
                B, seq_len, C = q.shape
                original_shape = extra_options.get("original_shape", None)
                h, w = _infer_spatial_dims(seq_len, original_shape)

                if h is None:
                    # Cannot determine spatial dims; leave q unchanged
                    return q, k, v

                windowed_out = _windowed_attention(q, k, v, h, w, _ws)
                # Blend original query with windowed-attention output
                new_q = q + _msw_s * (windowed_out - q)
                return new_q, k, v

            model.set_model_attn1_patch(msw_msa_attn1_patch)

        # ── RAU-Net ──────────────────────────────────────────────────────────
        if apply_rau_net and rau_net_strength > 0.0:
            _rau_s = rau_net_strength
            _threshold = rau_net_skip_threshold

            def rau_net_output_block_patch(h_feat, hsp, transformer_options):
                block = transformer_options.get("block", None)
                if block is not None and isinstance(block, (tuple, list)) and len(block) >= 2:
                    block_idx = int(block[1])
                else:
                    block_idx = 0

                if block_idx >= _threshold:
                    hsp = hsp * (1.0 - _rau_s)

                return h_feat, hsp

            model.set_model_output_block_patch(rau_net_output_block_patch)

        return (model,)


NODE_CLASS_MAPPINGS = {
    "HiDiffusionNode_PoP": HiDiffusionNode_PoP,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HiDiffusionNode_PoP": "HiDiffusion (PoP)",
}
