import os
import hashlib
from PIL import Image, ImageOps
import numpy as np
import torch

import folder_paths


class LoadImageResizer_PoP:
    CATEGORY = "image"
    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image"
    CATEGORY = "PoP"

    @classmethod
    def INPUT_TYPES(cls):
        """Define input types, including a slider for megapixels."""
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {
            "required": {
                "image": (sorted(files), {"image_upload": True}),
                "megapixels": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 64.0, "step": 0.01})
            },
        }

    

    @classmethod
    def VALIDATE_INPUTS(cls, image, megapixels):
        """Validate both the image and megapixels inputs."""
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        
        if megapixels <= 0:
            return "Megapixels must be a positive number."
        
        return True

    @classmethod
    def IS_CHANGED(cls, image):
        """Check if the image has changed."""
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    def load_image(self, image, megapixels):
        """Load and resize image based on user-defined megapixels."""
        # Load the image
        image_path = folder_paths.get_annotated_filepath(image)
        i = Image.open(image_path)
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")

        # Calculate new dimensions based on megapixels
        new_width, new_height = self.get_new_dimensions(image, megapixels, round_to=64)  # round to 8 or 64

        # Resize the image using the LANCZOS filter
        # For the main image
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)

        resized_image = np.array(resized_image).astype(np.float32) / 255.0
        resized_image = torch.from_numpy(resized_image)[None,]

        # Handle alpha channel (mask)
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0

            resized_mask = Image.fromarray(mask).resize((new_width, new_height), Image.LANCZOS),

        else:
            resized_mask = torch.zeros((new_height, new_width), dtype=torch.float32, device="cpu")
        
        return (resized_image, resized_mask)

    def get_new_dimensions(self, image, megapixels, round_to=8):
        """Calculate new dimensions based on megapixels and round to the nearest multiple of 'round_to'."""
        width, height = image.size
        new_width = int(np.sqrt(megapixels * 1000000 * width / height))
        new_height = int(new_width * height / width)
        
        # Round dimensions to the nearest multiple of 'round_to'
        new_width = ((new_width + round_to - 1) // round_to) * round_to
        new_height = ((new_height + round_to - 1) // round_to) * round_to
        
        return (new_width, new_height)

            
NODE_CLASS_MAPPINGS = {
    "LoadImageResizer_PoP": LoadImageResizer_PoP
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImageResizer_PoP": "Load Image Resizer PoP"    
}
