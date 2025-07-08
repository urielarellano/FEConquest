from PIL import Image
import os

input_folder = 'docs/assets/FatesPortraits'  # change this to your folder

for filename in os.listdir(input_folder):
    if filename.lower().endswith('.png'):
        png_path = os.path.join(input_folder, filename)
        
        # Open PNG image
        img = Image.open(png_path).convert("RGBA")  # keep transparency if any
        
        # Create new filename with .webp extension
        webp_filename = os.path.splitext(filename)[0] + '.webp'
        webp_path = os.path.join(input_folder, webp_filename)
        
        # Save as WebP (lossless=True keeps quality, you can also try lossy with quality param)
        img.save(webp_path, 'WEBP', lossless=True)
        
        # Delete original PNG
        os.remove(png_path)
        
        print(f'Converted {filename} to {webp_filename} and deleted original PNG.')
