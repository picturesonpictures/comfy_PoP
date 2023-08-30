import numpy as np
import cv2
from PIL import Image



def convert_to_3_channels(x):
    if x.dtype == np.float32:
        assert x.min() >= 0.0 and x.max() <= 1.0
        x = (255.0 * x).astype(np.uint8)
    elif x.dtype != np.uint8:
        raise ValueError("Unsupported dtype")
    x = np.squeeze(x, axis=0)
    if x.ndim == 2:
        x = x[:, :, None]
    assert x.ndim == 3
    H, W, C = x.shape
    assert C in (1, 3, 4)
    if C == 3:
        return x
    if C == 1:
        return np.repeat(x, 3, axis=2)
    if C == 4:
        color = x[:, :, :3].astype(np.float32)
        alpha = x[:, :, 3:4].astype(np.float32) / 255.0
        y = color * alpha + 255.0 * (1.0 - alpha)
        return y.clip(0, 255).astype(np.uint8)

# Resize an image to a resolution, preserving aspect ratio
def resize_to_resolution(input_image, resolution): 
    print("Resolution:", resolution) # Debug print
    H, W, C = input_image.shape # Debug print
    print("Input Shape:", H, W, C) # Debug print
    k = resolution / min(H, W)
    H_new = int(np.round(H * k / 64.0)) * 64
    W_new = int(np.round(W * k / 64.0)) * 64
    print("New Dimensions:", W_new, H_new) # Debug print
    interpolation = cv2.INTER_AREA if k < 1.0 else cv2.INTER_LINEAR
    resized_image = cv2.resize(input_image, (W_new, H_new), interpolation=interpolation)
    return resized_image 