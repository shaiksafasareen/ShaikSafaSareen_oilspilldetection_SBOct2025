"""
Script to create demo/test data for the oil spill detection app
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_demo_image(filename: str, width: int = 800, height: int = 600, 
                     has_spill: bool = True, spill_count: int = 3):
    """
    Create a demo image with or without oil spills
    
    Args:
        filename: Output filename
        width: Image width
        height: Image height
        has_spill: Whether to include oil spills
        spill_count: Number of spills to add
    """
    # Create base image (ocean/water scene)
    img = Image.new('RGB', (width, height), color=(70, 130, 180))  # Steel blue
    
    draw = ImageDraw.Draw(img)
    
    # Add some texture (waves)
    for y in range(0, height, 20):
        alpha = int(30 * np.sin(y / 50))
        color = (70 + alpha, 130 + alpha, 180 + alpha)
        draw.rectangle([(0, y), (width, y + 10)], fill=color)
    
    if has_spill:
        # Add oil spill patches (dark, iridescent colors)
        np.random.seed(42)  # For reproducibility
        for i in range(spill_count):
            x = np.random.randint(100, width - 100)
            y = np.random.randint(100, height - 100)
            size = np.random.randint(50, 150)
            
            # Create oil spill (dark, rainbow-like)
            for offset in range(size):
                alpha = int(255 * (1 - offset / size))
                color = (
                    max(0, 20 - offset // 10),
                    max(0, 30 - offset // 10),
                    max(0, 40 - offset // 10)
                )
                draw.ellipse(
                    [(x - size + offset, y - size + offset),
                     (x + size - offset, y + size - offset)],
                    fill=color,
                    outline=None
                )
    
    # Add some text label
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    label = "Oil Spill" if has_spill else "Clean Water"
    text_color = (255, 0, 0) if has_spill else (0, 255, 0)
    draw.text((10, 10), label, fill=text_color, font=font)
    
    # Save image
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)
    print(f"Created: {filename}")

def create_demo_dataset():
    """Create a set of demo images"""
    demo_dir = "demo_images"
    os.makedirs(demo_dir, exist_ok=True)
    
    # Create various scenarios
    scenarios = [
        ("clean_water_1.jpg", 800, 600, False, 0),
        ("clean_water_2.jpg", 1024, 768, False, 0),
        ("oil_spill_small.jpg", 800, 600, True, 1),
        ("oil_spill_medium.jpg", 800, 600, True, 3),
        ("oil_spill_large.jpg", 1024, 768, True, 5),
        ("oil_spill_multiple.jpg", 1200, 900, True, 8),
    ]
    
    for filename, width, height, has_spill, count in scenarios:
        filepath = os.path.join(demo_dir, filename)
        create_demo_image(filepath, width, height, has_spill, count)
    
    print(f"\n✅ Created {len(scenarios)} demo images in {demo_dir}/")
    print("You can use these images to test the oil spill detection system!")

if __name__ == "__main__":
    create_demo_dataset()

