
from .AnyAspectRatio import NODE_CLASS_MAPPINGS as AnyAspectRatio_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as AnyAspectRatio_DISPLAY_NAME_MAPPINGS
from .LoraStackLoader_PoP import NODE_CLASS_MAPPINGS as LoraStackLoader_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoraStackLoader_PoP_DISPLAY_NAME_MAPPINGS
from .LoraStackLoader10_PoP import NODE_CLASS_MAPPINGS as LoraStackLoader10_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoraStackLoader10_PoP_DISPLAY_NAME_MAPPINGS
from .AdaptiveCannyDetector_PoP import NODE_CLASS_MAPPINGS as AdaptiveCannyDetector_PoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as AdaptiveCannyDetector_PoP_DISPLAY_NAME_MAPPINGS
from .VAEEncodeDecodeLoader import NODE_CLASS_MAPPINGS as VAEEncoderPoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as VAEEncoderPoP_DISPLAY_NAME_MAPPINGS
from .VAEEncodeDecodeLoader import NODE_CLASS_MAPPINGS as VAEDecoderPoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as VAEDecoderPoP_DISPLAY_NAME_MAPPINGS
from .ConditioningPoP import NODE_CLASS_MAPPINGS as ConditioningMultiplierPoP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as ConditioningMultiplierPoP_DISPLAY_NAME_MAPPINGS   

NODE_CLASS_MAPPINGS = {
    **AnyAspectRatio_MAPPINGS,
    **LoraStackLoader_PoP_MAPPINGS,
    **LoraStackLoader10_PoP_MAPPINGS,
    **AdaptiveCannyDetector_PoP_MAPPINGS,
    **VAEEncoderPoP_MAPPINGS,
    **VAEDecoderPoP_MAPPINGS,
    **ConditioningMultiplierPoP_MAPPINGS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **AnyAspectRatio_DISPLAY_NAME_MAPPINGS,
    **LoraStackLoader_PoP_DISPLAY_NAME_MAPPINGS,
    **LoraStackLoader10_PoP_DISPLAY_NAME_MAPPINGS,
    **AdaptiveCannyDetector_PoP_DISPLAY_NAME_MAPPINGS,
    **VAEEncoderPoP_DISPLAY_NAME_MAPPINGS,
    **VAEDecoderPoP_DISPLAY_NAME_MAPPINGS,
    **ConditioningMultiplierPoP_DISPLAY_NAME_MAPPINGS,
    
}


