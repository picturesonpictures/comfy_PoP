class AspectRatio:
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
            },
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")

    FUNCTION = "calculate"

    CATEGORY = "Utilities"

    def calculate(self, width_ratio, height_ratio):
        # Calculate the width and height based on the input ratios
        total_pixels = 1024**2
        width = int((total_pixels * width_ratio / (width_ratio + height_ratio))**0.5)
        height = int((total_pixels * height_ratio / (width_ratio + height_ratio))**0.5)
        return (width, height)


# Dictionary that contains all nodes to export with their names
NODE_CLASS_MAPPINGS = {
    "AspectRatio": AspectRatio
}

# Dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "AspectRatio": "Aspect Ratio Node"
}
