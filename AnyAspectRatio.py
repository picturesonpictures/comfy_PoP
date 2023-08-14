{
  "nbformat": 4,
  "nbformat_minor": 5,
  "metadata": {
    "noteable-chatgpt": {
      "create_notebook": {
        "openai_conversation_id": "d115f49d-1947-57fa-8f60-c3a9992a88f9",
        "openai_ephemeral_user_id": "299bf4b1-948b-5551-b771-353c19998972",
        "openai_subdivision1_iso_code": "US-TX"
      }
    },
    "kernel_info": {
      "name": "python3"
    },
    "noteable": {
      "last_transaction_id": "a2f68e05-b771-4645-b857-6199ed6099c7"
    },
    "kernelspec": {
      "display_name": "Python 3.9",
      "language": "python",
      "name": "python3"
    },
    "selected_hardware_size": "small"
  },
  "cells": [
    {
      "id": "6605f565-bd1e-4ede-be24-5dfca13f44c1",
      "cell_type": "code",
      "metadata": {
        "noteable": {
          "cell_type": "code"
        }
      },
      "execution_count": null,
      "source": "import math\n\ndef calculate_dimensions(a, b):\n    # Calculate the aspect ratio\n    r = a / b\n\n    # Calculate the height and width\n    height = math.sqrt((1024**2 * b) / a)\n    width = r * height\n\n    # Round to integers\n    height = int(round(height))\n    width = int(round(width))\n\n    return width, height\n\n# Example usage\na = 16\nb = 9\nwidth, height = calculate_dimensions(a, b)\nwidth, height",
      "outputs": []
    },
    {
      "id": "6bfe2baf-d000-46a4-8322-d63b24cae7f7",
      "cell_type": "code",
      "metadata": {
        "noteable": {
          "cell_type": "code"
        }
      },
      "execution_count": null,
      "source": "# Import ComfyUI library (please replace with the correct import statement)\n# import comfyui as ui\n\n# Define the ComfyUI node\n# node = ui.Node('Aspect Ratio Node')\n\n# Add input widgets for width and height ratios\n# width_ratio_widget = ui.TextInput('Width Ratio')\n# height_ratio_widget = ui.TextInput('Height Ratio')\n# node.add_input(width_ratio_widget)\n# node.add_input(height_ratio_widget)\n\n# Function to calculate and display dimensions\ndef on_input_change():\n    a = int(width_ratio_widget.value)\n    b = int(height_ratio_widget.value)\n    width, height = calculate_dimensions(a, b)\n    # Display the output (please replace with the correct ComfyUI syntax)\n    # ui.Label(f'Width: {width}, Height: {height}')\n\n# Connect the input change event to the function\n# width_ratio_widget.on_change(on_input_change)\n# height_ratio_widget.on_change(on_input_change)",
      "outputs": []
    }
  ]
}