class ConditioningMultiplier_PoP:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"conditioning": ("CONDITIONING", ), "multiplier": ("FLOAT", {"default": 1.0, "min": -1, "max": 3.0})}}

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "multiply_conditioning_strength"
    CATEGORY = "PoP"
    
    def multiply_conditioning_strength(self, conditioning, multiplier):
        # Validate the input types for 'conditioning' and 'multiplier'
        if not isinstance(conditioning, list) or not isinstance(multiplier, float):
            raise ValueError("Invalid input types")

        #Initialize a new list to store the modified conditioning objects
        new_conditioning = []

        # Iterate through each element in the 'conditioning' list
        for index, (tensor, attributes) in enumerate(conditioning):
            # Multiply the tensor by the given multiplier
            new_tensor = tensor.clone()
            new_attributes = attributes.copy()

            # Multiply the new tensor by the given multiplier
            new_tensor *= multiplier

            # If 'pooled_output' exists, scale it by the multiplier
            if "pooled_output" in attributes:
                new_pooled_output = attributes["pooled_output"].clone()
                new_pooled_output *= multiplier
                new_attributes["pooled_output"] = new_pooled_output

            # Add the modified tensor and attributes to the new_conditioning list
            new_conditioning.append([new_tensor, new_attributes])


        # Return the modified 'conditioning' object
        return (new_conditioning, )  # NOTE: Returning new_conditioning here

class ConditioningNormalizer_PoP:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"conditioning": ("CONDITIONING", )}}

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "normalize_conditioning"
    CATEGORY = "PoP"

    def normalize_conditioning(self, conditioning):
        # Validate the input type for 'conditioning'
        if not isinstance(conditioning, list):
            raise ValueError("Invalid input type")

        # Initialize a new list to store the modified conditioning objects
        new_conditioning = []

        # Iterate through the 'conditioning' list
        for index, (tensor, attributes) in enumerate(conditioning): #Q what is this doing? A iterating through the conditioning list
            # Create new objects to store modified tensor and attributes
            new_tensor = tensor.clone()
            new_attributes = attributes.copy()

            # Normalize the new tensor to have zero mean and unit variance
            new_tensor -= new_tensor.mean()
            new_tensor /= new_tensor.std()

            # If 'pooled_output' exists, normalize it
            if "pooled_output" in attributes:
                new_pooled_output = attributes["pooled_output"].clone()
                new_pooled_output -= new_pooled_output.mean()
                new_pooled_output /= new_pooled_output.std()
                new_attributes["pooled_output"] = new_pooled_output

            # Add the modified tensor and attributes to the new_conditioning list
            new_conditioning.append([new_tensor, new_attributes])

        # Return the modified 'conditioning' object
        return (new_conditioning, )  # NOTE: Returning new_conditioning here

#create node class mappings and node display name mappings
NODE_CLASS_MAPPINGS = {
    "ConditioningMultiplier_PoP": ConditioningMultiplier_PoP,
    "ConditioningNormalizer_PoP": ConditioningNormalizer_PoP
} 
NODE_DISPLAY_NAME_MAPPINGS = {
    "ConditioningMultiplier_PoP": "Conditioning Multiplier PoP",
    "ConditioningNormalizer_PoP": "Conditioning Normalizer PoP"
}