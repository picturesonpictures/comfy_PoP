class AnyAspectRatio:
    """
    An aspect ratio node

    This node takes width and height ratios and calculates the corresponding width and height values.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width_ratio": ("INT", {
                    "default": 16,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "height_ratio": ("INT", {
                    "default": 9,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "side_length": ("INT", {
                    "default": 1024,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "rounding_value": ("INT", {
                    "default": 64,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
            },
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")

    FUNCTION = "calculate"

    CATEGORY = "PoP"

    # Calculate the width and height based on the input ratios
    def calculate(self, width_ratio, height_ratio, side_length, rounding_value):
        total_pixels = side_length**2
        width = int((total_pixels * width_ratio / (width_ratio + height_ratio))**0.5)
        height = int((total_pixels * height_ratio / (width_ratio + height_ratio))**0.5)
        width = int((total_pixels * width_ratio / height_ratio)**0.5)
        height = int((total_pixels * height_ratio / width_ratio)**0.5)
        
        # Rounding the width and height to the nearest multiple of rounding_value
        width = (width // rounding_value) * rounding_value
        height = (height // rounding_value) * rounding_value

        return (width, height)
        
# Dictionary that contains all nodes to export with their names
NODE_CLASS_MAPPINGS = {
    "AnyAspectRatio": AnyAspectRatio
}

# A dictionary that contains the friendly/humanly readable titles for the nodes. yes hello, thank you for reading this far.
NODE_DISPLAY_NAME_MAPPINGS = {
    "AnyAspectRatio": "AnyAspectRatio"
}
