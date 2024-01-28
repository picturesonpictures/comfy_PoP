import openai
import logging
import requests
import os
import time
import torchvision.transforms as transforms
import numpy as np
from PIL import Image
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
        # Configure logging
        logging.basicConfig(filename='image_generation_logs.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        # Get the API key from an environment variable
        openai.api_key = os.getenv('OPENAI_API_KEY')
        # Define the directory to save images in
        self.image_dir = 'generated_images'
        # Create the directory if it doesn't exist
        os.makedirs(self.image_dir, exist_ok=True)

    def generate_image(self, prompt, image_size='1792x1024', image_quality='standard', style='natural'):
        # Check if the API key is set
        if openai.api_key is None:
            logging.warning("OpenAI API key is not set. Returning default image.")
            # Load and return the default image
            default_image_path = 'custom_nodes\\comfy_PoP\\OPENAI_API_KEY_NOT_SET.png'
            try:
                default_image = Image.open(default_image_path).convert('RGB')
            except FileNotFoundError:
                logging.error(f"File not found: {default_image_path}")
                return "Error: Default image not found."
            transform = transforms.Compose([transforms.ToTensor()])
            default_image_tensor = transform(default_image).unsqueeze(0)
            default_image_tensor = default_image_tensor.permute(0, 2, 3, 1)
            return (default_image_tensor, )
        try:
            response = openai.Image.create(
                model='dall-e-3',
                prompt=prompt,
                n=1,
                size=image_size,
                quality=image_quality,
                style=style
            )
            logging.info(f'API Response: {response}')
            image_url = response['data'][0]['url']

            # Download and save the image, then convert to tensor
            return self.save_api_image_and_convert_to_tensor(image_url)

        except openai.error.AuthenticationError:
            logging.error("Authentication failed: Invalid API key.")
            return "Error: Authentication failed. Please check your API key."
        
        except openai.error.RateLimitError:
            logging.error("Rate limit exceeded.")
            return "Error: Rate limit exceeded. Please try again later."

        except openai.error.InvalidRequestError as e:
            logging.error(f"Invalid request: {e}")
            return f"Error: Invalid request. {e}"

        except requests.exceptions.RequestException as e:
            logging.error(f"Network error: {e}")
            return "Error: Network issue. Please check your internet connection."

        except openai.error.OpenAIError as e:
            # Generic catch-all for other OpenAI errors
            logging.error(f"OpenAI API error: {e}")
            return f"Error: An unexpected error occurred. {e}"

        except Exception as e:
            # Generic catch-all for any other error
            logging.error(f"Unexpected error: {e}")
            return "Error: An unexpected error occurred. Please try again."




    def save_api_image_and_convert_to_tensor(self, image_url):
        try:
            # Download and save the image
            image_response = requests.get(image_url, stream=True)
            if image_response.status_code == 200:
                filename = f'image_{int(time.time())}.png'
                filepath = os.path.join(self.image_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(image_response.content)
                logging.info(f'Image saved: {filepath}')

                # Open the saved image file with PIL
                image = Image.open(filepath).convert('RGB')

            # Convert the image to a tensor
            transform = transforms.Compose([
                transforms.ToTensor(),  # Normalizes pixel values between 0 and 1
            ])
            image_tensor = transform(image).unsqueeze(0)  # Adds batch dimension


            # Change tensor shape from (1, 3, height, width) to (1, height, width, 3)
            image_tensor = image_tensor.permute(0, 2, 3, 1)
            return (image_tensor, )

        except Exception as e:
            logging.error(f'Error in saving API image and converting to tensor: {e}')
            return None


# Node registration
NODE_CLASS_MAPPINGS = {"DallE3_PoP": DallE3_PoP}
NODE_DISPLAY_NAME_MAPPINGS = {"DallE3_PoP": "DALL-E 3 Generator"}