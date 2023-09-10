# VAE Encode Decode Loader
import numpy as np
import os
import sys
import folder_paths
import comfy.sd
#we need proper documentation for this class
# singleton VAE model loader
class VAEModel:
    _instances = {}

    @classmethod
    def get_instance(cls, vae_path):
        if vae_path not in cls._instances:
            cls._instances[vae_path] = comfy.sd.VAE(ckpt_path=vae_path)
        return cls._instances[vae_path]

# VAE Encoder node
class VAEEncoderPoP:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "pixels": ("IMAGE", ),
                "vae_name": (folder_paths.get_filename_list("vae"), )
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("samples",)
    FUNCTION = "encode"

    def vae_encode_crop_pixels(self, pixels):
        height, width, _ = pixels.shape[1:]
        new_dim = min(height, width)
        height_start = (height - new_dim) // 2
        width_start = (width - new_dim) // 2
        cropped_pixels = pixels[:, height_start:height_start + new_dim, width_start:width_start + new_dim, :]
        return cropped_pixels

    def encode(self, vae_name, pixels):
        vae_path = folder_paths.get_full_path('vae', vae_name)
        vae = VAEModel.get_instance(vae_path)
        pixels = self.vae_encode_crop_pixels(pixels)
        encoded = vae.encode(pixels[:,:,:,:3])
        return ({"samples": encoded}, )

# VAE Decoder node
class VAEDecoderPoP:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "samples": ("LATENT", ),
                "vae_name": (folder_paths.get_filename_list("vae"), )
            }
        }

    RETURN_TYPES = ("IMAGE",)

    FUNCTION = "decode"
    
# decode function
    def decode(self, vae_name, samples):
        print("vae_name", vae_name)
        print("samples", samples)
        vae_path = folder_paths.get_full_path('vae', vae_name)
        print("vae_path", vae_path)
        vae = VAEModel.get_instance(vae_path)
        print("vae", vae)
        decoded = (vae.decode(samples["samples"]), )        
        print("decoded", decoded)

        return decoded

NODE_CLASS_MAPPINGS = {
    "VAEEncoderPoP": VAEEncoderPoP,
    "VAEDecoderPoP": VAEDecoderPoP
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "VAEEncoderPoP": "VAE Encoder PoP",
    "VAEDecoderPoP": "VAE Decoder PoP"
}


