from PIL import Image
import os

input_path = "/home/vscode/.gemini/antigravity/brain/f1730b16-c9bf-43e4-acb4-b84bf142cffd/strake_logo_final_1767087079702.png"
output_path = "/workspaces/rust-postgres/strake-landing-page/strake_logo.png"

try:
    img = Image.open(input_path)
    width, height = img.size
    
    # Crop the middle vertical third
    left = width / 3
    right = 2 * width / 3
    
    # Basic crop
    img_middle = img.crop((left, 0, right, height))
    
    # Optional: Trim whitespace? 
    # Let's trust the user just wants the middle section for now. 
    # Generative images usually have white backgrounds. 
    # Let's try to get the bounding box of non-white content to make it cleaner.
    
    # Convert to RGBA just in case
    img_middle = img_middle.convert("RGBA")
    
    # Create a mask of non-white pixels (assuming white bg)
    # Actually, the user asked for "White background", so we can make it transparent if we want,
    # or just trim the white space.
    # Let's just save the cropped third first to ensure we get the logo. 
    # Trimming might remove the "Strake" text if it's small or detached.
    
    img_middle.save(output_path)
    print(f"Successfully cropped middle logo to {output_path}")

except Exception as e:
    print(f"Error processing image: {e}")
