from PIL import Image
import os

input_folder = 'docs/assets/FatesPortraits'
output_folder = 'docs/assets/FatesPortraits/resized'

scale_factor = 0.2
quality = 100

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith('.webp'):
        filepath = os.path.join(input_folder, filename)
        img = Image.open(filepath)

        # Calculate new size
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)

        # Resize with ANTIALIAS for better quality
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)

        output_path = os.path.join(output_folder, filename)
        img_resized.save(output_path, 'WEBP', quality=quality)

        print(f'Scaled {filename} from {img.width}x{img.height} to {new_width}x{new_height}')
