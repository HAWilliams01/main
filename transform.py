from PIL import Image
import os
import sys

input_dir = "./inputImages"
output_dir = "./outputImages"

# Transform images to a specific aspect ratio
# Usage: python3 transform.py
# portrait 10 / 16, square 1 / 1, traditional 4 / 3, computer 16 / 10, hd 16 / 9, widescreen 1.85 / 1, cinema 2.39 / 1, banner 4 / 1

# Get target aspect ratio from user
try:
    input_aspect_ratio = input("Enter target aspect ratio (10/16, 1/1, 4/3, 16/10, 16/9, 1.85/1, 2.39/1, 4/1): ")
    cleaned_input = input_aspect_ratio.replace(" ", "").replace(",", "/").replace(":", "/").replace(";", "/")
    target_aspect_ratio = float(eval(cleaned_input))
except (SyntaxError, NameError, ZeroDivisionError):
    print("Error: Invalid aspect ratio provided. Please use a valid format like '4/3' or '1.85 / 1'.")
    sys.exit(1)

if target_aspect_ratio <= 0:
    print("Error: Aspect ratio must be greater than zero.")
    sys.exit(1)


def match_aspect_ratio_title(aspect_ratio):
    match aspect_ratio:
        case "10/16":
            result = "portrait"
        case "1/1":
            result = "square"
        case "4/3":
            result = "traditional"
        case "16/10":
            result = "computer"
        case "16/9":
            result = "landscape"
        case "1.85/1":
            result = "widescreen"
        case "2.39/1":
            result = "cinema"
        case "4/1":
            result = "banner"
        case _:
            result = ""
    return result

background_type = input("Enter background type ('white' for solid white or 'transparent' for transparency: ").strip().lower()

for files in os.listdir(input_dir):
    image = Image.open(os.path.join(input_dir, files))
    filename = os.path.splitext(files)[0]
    extension = os.path.splitext(files)[1]
    
    original_width = image.width
    original_height = image.height

    # Calculate new dimensions
    if original_width / original_height > target_aspect_ratio:
        # Wider than, adjust height - add 10px buffer
        new_width = original_width + 10
        new_height = int(original_width / target_aspect_ratio)
    else:
        # Taller than, adjust width - add 10px buffer
        new_height = original_height + 10
        new_width = int(original_height * target_aspect_ratio)

    # TODO add option for transparent background
    if background_type == "white":
        if image.mode != "RGB":
            image = image.convert("RGB")
        transformed_image = Image.new(image.mode, (new_width, new_height), (255, 255, 255))
    elif background_type == "transparent":
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        transformed_image = Image.new(image.mode, (new_width, new_height), (0, 0, 0, 0))
    else:
        print("Error: Invalid background type. Use 'white' or 'transparent'.")
        sys.exit(1)

    # Center original image on canvas
    offset_x = (new_width - original_width) // 2
    offset_y = (new_height - original_height) // 2
    transformed_image.paste(image, (offset_x, offset_y))
    
    # Save transformed image
    aspect_ratio_title_result = match_aspect_ratio_title(cleaned_input)
    print(aspect_ratio_title_result)
    transformed_image.save(os.path.join(output_dir, f"{filename}-{aspect_ratio_title_result}{extension}"))