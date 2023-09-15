from .AnyAspectRatio import NODE_CLASS_MAPPINGS as AnyAspectRatio_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as AnyAspectRatio_DISPLAY_NAME_MAPPINGS
from .LoraStackLoader_PoP import NODE_CLASS_MAPPINGS as LoraStackLoader_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoraStackLoader_PoP_DISPLAY_NAME_MAPPINGS
from .LoraStackLoader10_PoP import NODE_CLASS_MAPPINGS as LoraStackLoader10_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoraStackLoader10_PoP_DISPLAY_NAME_MAPPINGS
from .AdaptiveCannyDetector_PoP import NODE_CLASS_MAPPINGS as AdaptiveCannyDetector_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as AdaptiveCannyDetector_PoP_DISPLAY_NAME_MAPPINGS
from .LoadImageResizer_PoP import NODE_CLASS_MAPPINGS as LoadImageResizer_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoadImageResizer_PoP_DISPLAY_NAME_MAPPINGS
from .Conditioning_PoP import NODE_CLASS_MAPPINGS as Conditioning_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as Conditioning_PoP_DISPLAY_NAME_MAPPINGS
from .VAEEncodeDecodeLoader_PoP import NODE_CLASS_MAPPINGS as VAEEncodeDecodeLoader_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as VAEEncodeDecodeLoader_PoP_DISPLAY_NAME_MAPPINGS 

NODE_CLASS_MAPPINGS = {
    **AnyAspectRatio_MAPPINGS,
    **LoraStackLoader_PoP_MAPPINGS,
    **LoraStackLoader10_PoP_MAPPINGS,
    **AdaptiveCannyDetector_PoP_MAPPINGS,
    **LoadImageResizer_PoP_MAPPINGS,
    **Conditioning_PoP_MAPPINGS,
    **VAEEncodeDecodeLoader_PoP_MAPPINGS
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **AnyAspectRatio_DISPLAY_NAME_MAPPINGS,
    **LoraStackLoader_PoP_DISPLAY_NAME_MAPPINGS,
    **LoraStackLoader10_PoP_DISPLAY_NAME_MAPPINGS,
    **AdaptiveCannyDetector_PoP_DISPLAY_NAME_MAPPINGS,
    **LoadImageResizer_PoP_DISPLAY_NAME_MAPPINGS,
    **Conditioning_PoP_DISPLAY_NAME_MAPPINGS,
    **VAEEncodeDecodeLoader_PoP_DISPLAY_NAME_MAPPINGS
}


__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]