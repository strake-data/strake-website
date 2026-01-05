from PIL import Image
import numpy as np

input_path = "/workspaces/rust-postgres/strake-landing-page/strake_logo.png"
output_path = "/workspaces/rust-postgres/strake-landing-page/strake_logo.png"

# Target Color: Hero Font Color (#1E3A8A -> 30, 58, 138)
target_color = (30, 58, 138)

# Cyan to replace: #06B6D4 -> (6, 182, 212)
# We need a threshold to catch anti-aliasing
cyan_target = np.array([6, 182, 212])

try:
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)
    
    # Calculate euclidean distance in RGB space to find "Cyan-ish" pixels
    r, g, b, a = data.T
    
    # Extract RGB only for distance calc
    rgb = data[..., :3]
    
    # Calculate distance from Cyan target
    # Use a relatively generous threshold to capture gradients/anti-aliasing
    # But be careful not to catch the white background or deep navy.
    diff = np.sqrt(np.sum((rgb - cyan_target) ** 2, axis=2))
    
    # Threshold - let's say pixels within 100 units 
    # (Deep Navy #0F172A is dist ~150 from Cyan, White is ~260, so 100 is safe)
    mask = diff < 120
    
    # Apply replacement
    data[mask, 0] = target_color[0] # R
    data[mask, 1] = target_color[1] # G
    data[mask, 2] = target_color[2] # B
    
    # Reconstruct image
    new_img = Image.fromarray(data)
    new_img.save(output_path)
    print(f"Successfully recolored Cyan pixels to {target_color}")

except Exception as e:
    print(f"Error processing image: {e}")
