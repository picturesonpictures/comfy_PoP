import torch
import cv2
import numpy as np
from PIL import Image
from .CNutil import convert_to_3_channels  # Assuming this function exists

class AdaptiveCannyDetector_PoP:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
#                "canny_low_threshold": ("FLOAT", {"default": 100.0, "min": 0.0, "max": 255.0, "step": 1.0, "description": "Canny low threshold"}),
#                "canny_high_threshold": ("FLOAT", {"default": 200.0, "min": 0.0, "max": 255.0, "step": 1.0, "description": "Canny high threshold"}),
                "gaussian_blur_ksize": ("INT", {"default": 5, "min": 1, "max": 31, "step": 1, "description": "Gaussian blur kernel size (if even +1 for odd)"}),
                "gaussian_blur_sigma": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 10.0, "step": 0.1, "description": "Gaussian blur sigma"}),
                "adaptive_thresh_method": (["GAUSSIAN_C", "MEAN_C"],),
                "adaptive_thresh_type": (["BINARY", "BINARY_INV"],),
                "adaptive_thresh_blocksize": ("INT", {"default": 11, "min": 3, "max": 51, "step": 1, "description": "Adaptive threshold block size (if even +1 for odd)"}),
                "adaptive_thresh_C": ("INT", {"default": 2, "min": 0, "max": 10, "step": 1, "description": "Adaptive threshold constant"})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    Category = "PoP"

    @classmethod
    def execute(s, images, gaussian_blur_ksize, gaussian_blur_sigma, adaptive_thresh_method, adaptive_thresh_type, adaptive_thresh_blocksize, adaptive_thresh_C):
        if not isinstance(images, list):
            images = [images]

        # Hardcoded Canny thresholds
        canny_low_threshold = 100
        canny_high_threshold = 200

        # Make gaussian_blur_ksize and adaptive_thresh_blocksize odd, capping at max value
        gaussian_blur_ksize = min(31, gaussian_blur_ksize + (gaussian_blur_ksize % 2 == 0))
        adaptive_thresh_blocksize = min(51, adaptive_thresh_blocksize + (adaptive_thresh_blocksize % 2 == 0))

        processed_images = []
        for img in images:
            img = convert_to_3_channels(img.cpu().numpy())
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply Gaussian Blur
            blurred_img = cv2.GaussianBlur(gray_img, (gaussian_blur_ksize, gaussian_blur_ksize), gaussian_blur_sigma)
            
            # Determine adaptive method and threshold type based on input parameters
            adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C if adaptive_thresh_method == "GAUSSIAN_C" else cv2.ADAPTIVE_THRESH_MEAN_C
            threshold_type = cv2.THRESH_BINARY if adaptive_thresh_type == "BINARY" else cv2.THRESH_BINARY_INV

            # Apply Adaptive Thresholding
            adapt_thresh_img = cv2.adaptiveThreshold(
                blurred_img, 255, adaptive_method, threshold_type, 
                adaptive_thresh_blocksize, adaptive_thresh_C
            )

            
            # Apply Canny edge detection
            edges = cv2.Canny(adapt_thresh_img, int(canny_low_threshold), int(canny_high_threshold))
            
            edges_3_channel = cv2.merge([edges, edges, edges])
            processed_images.append(edges_3_channel)

        output_tensor = torch.stack([torch.tensor(np_img) for np_img in processed_images])
        output_tensor = output_tensor.to(torch.float32)
        output_tensor = output_tensor / 255.0  # Normalize to [0, 1]
        return (output_tensor,)

# Exports
NODE_CLASS_MAPPINGS = {
    "AdaptiveCannyDetector_PoP": AdaptiveCannyDetector_PoP 
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "AdaptiveCannyDetector_PoP": "AdaptiveCannyDetector_PoP" 
}
