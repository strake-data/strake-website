from PIL import Image, ImageChops

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im # no content found

input_path = "/workspaces/rust-postgres/strake-landing-page/strake_logo.png"

try:
    img = Image.open(input_path).convert("RGBA")
    
    # First, handle the white background if it exists by making it transparent?
    # Or just trim to content.
    # The user prompt said "White background". 
    # Let's try to make the white background transparent first for a cleaner look?
    # Actually, let's just trim the whitespace first.
    
    # We need to detect "whitespace" which is likely white #FFFFFF.
    # The trim function above compares to top-left pixel. 
    # If the top-left is white, it trims white.
    
    trimmed_img = trim(img)
    
    # Overwrite
    trimmed_img.save(input_path)
    print(f"Successfully trimmed whitespace from {input_path}")
    print(f"New size: {trimmed_img.size}")

except Exception as e:
    print(f"Error processing image: {e}")
