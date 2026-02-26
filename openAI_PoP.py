import logging
import os
import time

import requests
import torchvision.transforms as transforms
import numpy as np
from PIL import Image
from openai import OpenAI, AuthenticationError, RateLimitError, BadRequestError, APIConnectionError, APIError

_log_file = os.path.join(os.path.dirname(__file__), 'image_generation_logs.log')
logging.basicConfig(filename=_log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class DallE3_PoP:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image_size": (["1792x1024", "1024x1024", "1024x1792"],),
                "image_quality": (["standard", "hd"],),
                "style": (["vivid", "natural"], {"default": "natural"})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "AI Generation"

    def __init__(self):
        self.image_dir = os.path.join(os.path.dirname(__file__), 'generated_images')
        os.makedirs(self.image_dir, exist_ok=True)

    def generate_image(self, prompt, image_size='1792x1024', image_quality='standard', style='natural'):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logging.warning("OpenAI API key is not set. Returning default image.")
            default_image_path = os.path.join(os.path.dirname(__file__), 'OPENAI_API_KEY_NOT_SET.png')
            try:
                default_image = Image.open(default_image_path).convert('RGB')
            except FileNotFoundError:
                logging.error(f"Default image not found: {default_image_path}")
                return "Error: Default image not found."
            transform = transforms.Compose([transforms.ToTensor()])
            default_image_tensor = transform(default_image).unsqueeze(0)
            default_image_tensor = default_image_tensor.permute(0, 2, 3, 1)
            return (default_image_tensor,)

        client = OpenAI(api_key=api_key)
        try:
            response = client.images.generate(
                model='dall-e-3',
                prompt=prompt,
                n=1,
                size=image_size,
                quality=image_quality,
                style=style
            )
            logging.info(f'Image generated successfully.')
            image_url = response.data[0].url
            return self.save_api_image_and_convert_to_tensor(image_url)

        except AuthenticationError:
            logging.error("Authentication failed: Invalid API key.")
            return "Error: Authentication failed. Please check your API key."

        except RateLimitError:
            logging.error("Rate limit exceeded.")
            return "Error: Rate limit exceeded. Please try again later."

        except BadRequestError as e:
            logging.error(f"Invalid request: {e}")
            return f"Error: Invalid request. {e}"

        except APIConnectionError as e:
            logging.error(f"Network error: {e}")
            return "Error: Network issue. Please check your internet connection."

        except APIError as e:
            logging.error(f"OpenAI API error: {e}")
            return f"Error: An unexpected API error occurred. {e}"

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return "Error: An unexpected error occurred. Please try again."

    def save_api_image_and_convert_to_tensor(self, image_url):
        try:
            image_response = requests.get(image_url, stream=True)
            if image_response.status_code == 200:
                filename = f'image_{int(time.time())}.png'
                filepath = os.path.join(self.image_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(image_response.content)
                logging.info(f'Image saved: {filepath}')
                image = Image.open(filepath).convert('RGB')
            else:
                logging.error(f"Failed to download image, status: {image_response.status_code}")
                return None

            transform = transforms.Compose([transforms.ToTensor()])
            image_tensor = transform(image).unsqueeze(0)
            image_tensor = image_tensor.permute(0, 2, 3, 1)
            return (image_tensor,)

        except Exception as e:
            logging.error(f'Error saving image and converting to tensor: {e}')
            return None


# Node registration
NODE_CLASS_MAPPINGS = {
    "DallE3_PoP": DallE3_PoP
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DallE3_PoP": "DALL-E 3 Generator"
}
