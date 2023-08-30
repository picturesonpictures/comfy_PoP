from .AnyAspectRatio import NODE_CLASS_MAPPINGS as AnyAspectRatio_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as AnyAspectRatio_DISPLAY_NAME_MAPPINGS
from .LoraStackLoader_PoP import NODE_CLASS_MAPPINGS as LoraStackLoader_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoraStackLoader_PoP_DISPLAY_NAME_MAPPINGS
from .LoraStackLoader10_PoP import NODE_CLASS_MAPPINGS as LoraStackLoader10_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoraStackLoader10_PoP_DISPLAY_NAME_MAPPINGS
from .AdaptiveCannyDetector_PoP import NODE_CLASS_MAPPINGS as AdaptiveCannyDetector_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as AdaptiveCannyDetector_PoP_DISPLAY_NAME_MAPPINGS

NODE_CLASS_MAPPINGS = {
    **AnyAspectRatio_MAPPINGS,
    **LoraStackLoader_PoP_MAPPINGS,
    **LoraStackLoader10_PoP_MAPPINGS,
    **AdaptiveCannyDetector_PoP_MAPPINGS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **AnyAspectRatio_DISPLAY_NAME_MAPPINGS,
    **LoraStackLoader_PoP_DISPLAY_NAME_MAPPINGS,
    **LoraStackLoader10_PoP_DISPLAY_NAME_MAPPINGS,
    **AdaptiveCannyDetector_PoP_DISPLAY_NAME_MAPPINGS,
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
