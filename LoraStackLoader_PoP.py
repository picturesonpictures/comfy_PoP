import folder_paths
import os
import sys

# Add the path to the comfy directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

# Import the specific submodules you need
import comfy.utils

class LoraStackLoader_PoP:
    loras = ["None"] + folder_paths.get_filename_list("loras")

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "model": ("MODEL",),
                    "clip": ("CLIP",),
                    "switch_1": (["Off", "On"],),
                    "lora_name_1": (cls.loras,),
                    "strength_model_1": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "strength_clip_1": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "switch_2": (["Off", "On"],),
                    "lora_name_2": (cls.loras,),
                    "strength_model_2": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "strength_clip_2": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "switch_3": (["Off", "On"],),
                    "lora_name_3": (cls.loras,),
                    "strength_model_3": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "strength_clip_3": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                }}
    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "apply_loras"
    CATEGORY = "loaders"

    def apply_loras(self, model, clip, switch_1, lora_name_1, strength_model_1, strength_clip_1, switch_2, lora_name_2, strength_model_2, strength_clip_2, switch_3, lora_name_3, strength_model_3, strength_clip_3):
        loras = [
            (switch_1, lora_name_1, strength_model_1, strength_clip_1),
            (switch_2, lora_name_2, strength_model_2, strength_clip_2),
            (switch_3, lora_name_3, strength_model_3, strength_clip_3)
        ]
        loras = [l for l in loras if l[0] != 'None']

        for switch, lora_name, strength_model, strength_clip in loras:
            if switch == 'Off' or lora_name is None:
                continue  # Skip loading this LoRA if the switch is off or lora_name is None

            lora_path = folder_paths.get_full_path("loras", lora_name)
            if lora_path is None:
                # Handle the case where lora_path is None (e.g., log a warning, load a default LoRA, or simply continue)
                continue

            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            model, clip = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)


        return (model, clip)
    
    # Adding the NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS to the LoraStackLoader_PoP module

# Dictionary that contains all nodes to export with their names
NODE_CLASS_MAPPINGS = {
    "LoraStackLoader_PoP": LoraStackLoader_PoP
}

# A dictionary that contains the friendly/humanly readable titles for the nodes. Thank you for reading my blog.
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoraStackLoader_PoP": "LoraStackLoader_PoP"
}
