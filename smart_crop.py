from PIL import Image
import numpy as np

input_path = "/workspaces/rust-postgres/strake-landing-page/strake_logo.png"

try:
    img = Image.open(input_path).convert("RGBA")
    
    # Convert to numpy array
    data = np.array(img)
    
    # Extract RGB channels
    r, g, b, a = data.T
    
    # Define white threshold (e.g., > 240 for all channels)
    # We want to keep dark pixels.
    # Background is "white" (255, 255, 255)
    
    threshold = 240
    
    # Mask of pixels that are NOT white (dark content)
    # (r < threshold) | (g < threshold) | (b < threshold)
    mask = (r < threshold) | (g < threshold) | (b < threshold)
    
    # Find coordinates of non-white pixels
    coords = np.argwhere(mask.T) # Transpose back to (y, x)?? 
    # np.argwhere returns (row, col) -> (y, x)
    # data is (height, width, 4)
    # mask is (width, height) because of .T? 
    # Let's do it on the original shape.
    
    mask = (data[..., 0] < threshold) | (data[..., 1] < threshold) | (data[..., 2] < threshold)
    
    coords = np.argwhere(mask)
    
    if coords.size > 0:
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0) + 1  # Slice is exclusive
        
        # Crop
        cropped = img.crop((x0, y0, x1, y1))
        cropped.save(input_path)
        print(f"Smart cropped to: {cropped.size}")
    else:
        print("No content found to crop!")

except Exception as e:
    print(f"Error processing image: {e}")
