# comfy_PoP

And here we have an ever-expanding list of custom nodes for https://github.com/comfyanonymous/ComfyUI/ that might be useful or possibly ridiculous. I'd like to create things that walk the line between these two concepts

To install please navigate to your ComfyUI custom_nodes folder. 
Then run git clone https://github.com/picturesonpictures/comfy_PoP

AdaptiveCannyDetector detects edges and it's fast.

LoraStacLoader_PoP isn't exactly breaking new ground, but couldn't find a node that had all the attributes I was looking for so I put this together. 3 LoRAs, on-off switches, model and weight inputs and outputs. Simple and useful.

LoraStackLoader10_PoP, on the other hand, is a  bit ridiculous. Want to load 10 LoRAs in one place? Here's your chance. Each Slot comes with an on/off switch and it has identical inputs/outputs to the single LoRA loader.

![image](https://github.com/picturesonpictures/comfy_PoP/assets/118248359/b65e99a8-5aef-4e39-86cf-10879a986d20)


And finally, AnyAspectRatio is another simplish node. It converts the pixel count of a square image to pretty much any aspect ratio you want. You can also set the size of the square. This node will allow you to make very unreasonable things.

The default side length of 1024 (which corresponds to a 1-megapixel image) and rounding value of 64 are Stability recommended values for SDXL. if you're using SDXL I'd strongly recommend you not adjust these values. For 1.5 drop the side length to 512, and then if you're using one of the 2.1 models that are trained on 768x768 adjust accordingly. 

I question whether there's a viable use case for deviating from these values too much, but as AI enthusiast Mahatma Ghandi once said "Freedom is not worth having if it does not include the freedom to make mistakes."

![image](https://github.com/picturesonpictures/comfy_PoP/assets/118248359/54194301-fada-4700-a0a7-21d72223d641)

LoraStack
