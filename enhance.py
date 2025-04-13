from PIL import Image, ImageEnhance
import os

input_dir = "./inputImages"
output_dir = "./outputImages"

# Enhance images by 2X, 2.5X, and 3X
# Usage: python3 enhance.py

resize_factors = input("Enter the resize factors (e.g., 2, 2.5, 3): ")
resize_factors = resize_factors.replace(" ", "")
resize_factors = [float(factor) for factor in resize_factors.split(",")]
sharpen_factor = input("Enter the sharpen enhancement level. If you wouldn't like to sharpen the image enter 1 (e.g., 2.0): ")

for files in os.listdir(input_dir):
    filename = os.path.splitext(files)[0]
    extension = os.path.splitext(files)[1]

    if files.endswith((".jpg", ".jpeg", ".png", ".gif")):
        image = Image.open(os.path.join(input_dir, files))
        
        if image.mode != "RGB":
            image = image.convert("RGB")

        enhancer = ImageEnhance.Sharpness(image)
        enhanced_image = enhancer.enhance(float(sharpen_factor))

        for factor in resize_factors:
            resized_image = enhanced_image.resize((int(image.width * factor), int(image.width * factor)), Image.LANCZOS)
            resized_image.save(os.path.join(output_dir, f"{filename}_{factor}x{extension}"))
            print(f"Saved enhanced image: {filename}_{factor}x{extension}")
    else:
        print(f"Skipping non-image file: {files}")