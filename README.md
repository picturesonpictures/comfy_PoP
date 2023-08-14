# comfy_PoP
Simple node that converts the pixel count of a square image to pretty much any aspect ratio you want. You can also set the size of the square. This node will allow you to make very unreasonable things.

The default side length of 1024 (which corresponds to a 1 megapixel image) and rounding value of 64 are Stability recommended values for SDXL. if you're using SDXL I'd strongly recommend you not adjust these values. For 1.5 drop side length to 512, and then if you're using one of the 2.1 models that are trained on 768x768 adjust accordingly. 

I question whether there's a viable use case for deviating from these values too much, but as AI enthusiast Mahatma Ghandi once said "Freedom is not worth having if it does not include the freedom to make mistakes."
