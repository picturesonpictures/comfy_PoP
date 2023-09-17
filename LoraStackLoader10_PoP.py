import folder_paths
import os
import sys
import comfy.utils

# Add the path to the comfy directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

class LoraStackLoader10_PoP:
    loras = ["None"] + folder_paths.get_filename_list("loras")

    @classmethod
    def INPUT_TYPES(cls):
        input_types = {"required": {"model": ("MODEL",), "clip": ("CLIP",)}}
        for i in range(1, 11):
            input_types["required"].update({
                f"switch_{i}": (["Off", "On"],),
                f"lora_name_{i}": (cls.loras,),
                f"strength_model_{i}": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                f"strength_clip_{i}": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
            })
        return input_types

    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "apply_loras"
    CATEGORY = "loaders"

    def apply_loras(self, model, clip, 
                    switch_1=None, lora_name_1=None, strength_model_1=None, strength_clip_1=None, 
                    switch_2=None, lora_name_2=None, strength_model_2=None, strength_clip_2=None, 
                    switch_3=None, lora_name_3=None, strength_model_3=None, strength_clip_3=None, 
                    switch_4=None, lora_name_4=None, strength_model_4=None, strength_clip_4=None, 
                    switch_5=None, lora_name_5=None, strength_model_5=None, strength_clip_5=None, 
                    switch_6=None, lora_name_6=None, strength_model_6=None, strength_clip_6=None, 
                    switch_7=None, lora_name_7=None, strength_model_7=None, strength_clip_7=None, 
                    switch_8=None, lora_name_8=None, strength_model_8=None, strength_clip_8=None, 
                    switch_9=None, lora_name_9=None, strength_model_9=None, strength_clip_9=None, 
                    switch_10=None, lora_name_10=None, strength_model_10=None, strength_clip_10=None):

        loras = [
            (switch_1, lora_name_1, strength_model_1, strength_clip_1),
            (switch_2, lora_name_2, strength_model_2, strength_clip_2),
            (switch_3, lora_name_3, strength_model_3, strength_clip_3),
            (switch_4, lora_name_4, strength_model_4, strength_clip_4),
            (switch_5, lora_name_5, strength_model_5, strength_clip_5),
            (switch_6, lora_name_6, strength_model_6, strength_clip_6),
            (switch_7, lora_name_7, strength_model_7, strength_clip_7),
            (switch_8, lora_name_8, strength_model_8, strength_clip_8),
            (switch_9, lora_name_9, strength_model_9, strength_clip_9),
            (switch_10, lora_name_10, strength_model_10, strength_clip_10)
    ]

    # More code, everyone


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

# Dictionary that contains all nodes to export with their names
NODE_CLASS_MAPPINGS = {
    "LoraStackLoader10_PoP": LoraStackLoader10_PoP
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoraStackLoader10_PoP": "LoraStackLoader10_PoP"
}
