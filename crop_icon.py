from PIL import Image, ImageChops
import numpy as np

input_path = "/workspaces/rust-postgres/strake-landing-page/strake_logo.png"

try:
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)
    
    # 1. Detect non-white rows (content)
    # Define threshold for "white"
    threshold = 240
    # True if pixel is NOT white
    is_content = (data[..., 0] < threshold) | (data[..., 1] < threshold) | (data[..., 2] < threshold)
    
    # Sum content pixels across columns to get a row profile
    row_profile = np.sum(is_content, axis=1)
    
    # We expect: 
    # [Content - Icon] values > 0
    # [Gap] values == 0
    # [Content - Text] values > 0
    
    # Find indices where rows have content
    content_rows = np.where(row_profile > 0)[0]
    
    if len(content_rows) == 0:
        print("No content found!")
        exit()
        
    start_y = content_rows[0]
    end_y = content_rows[-1]
    
    # To remove the text at the bottom, we look for the largest "gap" in the content rows?
    # Or simply: The text is usually the smaller block at the bottom.
    
    # Let's iterate through the rows and find the gap.
    # We look for a sequence of 0s between two sequences of >0s.
    
    # Simple heuristic: The icon is the top block.
    # Find the first block of content.
    
    # Find changes in state (0 -> >0 or >0 -> 0)
    # A gap is a run of 0s.
    
    # Let's find the split point.
    split_y = -1
    
    # We iterate from top to bottom.
    in_block = False
    
    blocks = [] # (start, end)
    current_start = -1
    
    for y in range(len(row_profile)):
        has_content = row_profile[y] > 0
        
        if has_content and not in_block:
            in_block = True
            current_start = y
        elif not has_content and in_block:
            in_block = False
            blocks.append((current_start, y))
            
    if in_block:
        blocks.append((current_start, len(row_profile)))
        
    print(f"Found blocks (y-coordinates): {blocks}")
    
    # We assume Block 0 is the Icon, Block 1 is the Text.
    if len(blocks) >= 2:
        # Crop to Block 0 only
        icon_start, icon_end = blocks[0]
        
        # Add a little padding? user trimmed whitespace before.
        # Let's keep it tight.
        
        # We also need to trim X (width) for just that block.
        # Extract the crop of just those rows
        row_crop = img.crop((0, icon_start, img.width, icon_end))
        
        # Now trim whitespace from X axis (width)
        # Use simple bbox trim on the result
        bg = Image.new(row_crop.mode, row_crop.size, (255, 255, 255, 0)) # Transparent bg for diff? 
        # Actually our "trim" function earlier worked well.
        # Let's just use .getbbox() on the alpha channel if it exists or diff.
        
        # Since we converted to RGBA, we can use the alpha channel if we made it transparent?
        # But we didn't transform white to transparent in this script.
        # Let's use the invert/bbox method or just re-reuse the logic.
        
        # Easy way: invert and getbbox (works for black on white)
        # But we have colors.
        
        # Let's just crop to the content rows we found (Y) and then re-run our content detection on X.
        
        # X profile for the top block
        block_data = data[icon_start:icon_end, :]
        is_content_x = (block_data[..., 0] < threshold) | (block_data[..., 1] < threshold) | (block_data[..., 2] < threshold)
        col_profile = np.sum(is_content_x, axis=0)
        content_cols = np.where(col_profile > 0)[0]
        
        if len(content_cols) > 0:
            x_start = content_cols[0]
            x_end = content_cols[-1] + 1
            
            final_crop = img.crop((x_start, icon_start, x_end, icon_end))
            final_crop.save(input_path)
            print(f"Cropped to Icon: {final_crop.size}")
        else:
             print("Error finding X bounds")
    
    elif len(blocks) == 1:
        # Maybe already cropped? Or text is connected?
        print("Only one block found. Assuming it is the icon (or text is connected). Cropping to it.")
        icon_start, icon_end = blocks[0]
         # X trim logic again
        block_data = data[icon_start:icon_end, :]
        is_content_x = (block_data[..., 0] < threshold) | (block_data[..., 1] < threshold) | (block_data[..., 2] < threshold)
        col_profile = np.sum(is_content_x, axis=0)
        content_cols = np.where(col_profile > 0)[0]
        if len(content_cols) > 0:
            x_start = content_cols[0]
            x_end = content_cols[-1] + 1
            final_crop = img.crop((x_start, icon_start, x_end, icon_end))
            final_crop.save(input_path)
            print(f"Trimmed single block: {final_crop.size}")

except Exception as e:
    print(f"Error processing image: {e}")

