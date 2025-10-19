#!/usr/bin/env python
"""
Demo Image Generator - Works without API keys
Creates simple test coloring pages to verify the system is working
"""
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from services.image_generator import ImageGenerator
import os

def create_demo_coloring_page(prompt, output_path="demo_output.png"):
    """
    Create a demo coloring page without using the Stability AI API
    Useful for testing the image processing pipeline
    
    Args:
        prompt (str): Description of what to draw
        output_path (str): Where to save the output
    """
    print(f"\nCreating demo coloring page for: '{prompt}'")
    
    # Create a simple test image
    width, height = 512, 512
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw some shapes based on keywords
    keywords = prompt.lower().split()
    
    # Background shapes
    draw.rectangle([40, 40, width-40, height-40], outline='gray', width=2)
    
    # Draw different shapes based on keywords
    if any(word in keywords for word in ['cat', 'dog', 'animal', 'pet']):
        # Draw a simple cat/dog face
        draw.ellipse([150, 150, 362, 362], outline='black', width=3)  # Head
        draw.ellipse([180, 200, 230, 250], outline='black', width=2)  # Eye
        draw.ellipse([282, 200, 332, 250], outline='black', width=2)  # Eye
        draw.arc([200, 250, 312, 330], 0, 180, fill='black', width=2)  # Smile
        
    elif any(word in keywords for word in ['robot', 'machine']):
        # Draw a simple robot
        draw.rectangle([180, 180, 332, 380], outline='black', width=3)  # Body
        draw.rectangle([170, 150, 342, 200], outline='black', width=3)  # Head
        draw.ellipse([210, 165, 230, 185], outline='black', width=2)  # Eye
        draw.ellipse([282, 165, 302, 185], outline='black', width=2)  # Eye
        
    elif any(word in keywords for word in ['flower', 'plant', 'tree']):
        # Draw a simple flower
        center_x, center_y = 256, 256
        draw.ellipse([center_x-30, center_y-30, center_x+30, center_y+30], outline='black', width=3)  # Center
        # Petals
        for angle in range(0, 360, 60):
            import math
            x = center_x + 60 * math.cos(math.radians(angle))
            y = center_y + 60 * math.sin(math.radians(angle))
            draw.ellipse([x-25, y-25, x+25, y+25], outline='black', width=2)
            
    elif any(word in keywords for word in ['star', 'space', 'sky']):
        # Draw stars
        points = [(256, 150), (275, 210), (340, 210), (290, 250), 
                  (310, 315), (256, 280), (202, 315), (222, 250), 
                  (172, 210), (237, 210)]
        draw.polygon(points, outline='black', width=3)
        
    else:
        # Generic shapes
        draw.ellipse([150, 150, 362, 362], outline='black', width=3)
        draw.rectangle([200, 200, 312, 312], outline='black', width=2)
        draw.polygon([(256, 180), (220, 250), (292, 250)], outline='black', width=2)
    
    # Add decorative elements
    draw.ellipse([70, 70, 120, 120], outline='gray', width=2)
    draw.ellipse([392, 392, 442, 442], outline='gray', width=2)
    
    # Add text at bottom
    try:
        draw.text((256, 480), prompt[:30], fill='black', anchor='mm')
    except:
        pass
    
    # Now convert to coloring page style
    generator = ImageGenerator()
    coloring_page = generator._convert_to_coloring_page(img)
    
    # Save
    coloring_page.save(output_path)
    print(f"[OK] Demo coloring page saved to: {output_path}")
    print(f"     Open this file to see your coloring page!")
    
    return output_path

def test_image_processing():
    """Test the image processing pipeline"""
    print("\n" + "="*60)
    print("Testing Image Processing Pipeline")
    print("="*60)
    
    test_prompts = [
        "A cute cat",
        "A friendly robot",
        "A beautiful flower",
        "A shining star",
        "A happy dragon"
    ]
    
    output_dir = "demo_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    for i, prompt in enumerate(test_prompts, 1):
        output_file = os.path.join(output_dir, f"demo_{i}.png")
        create_demo_coloring_page(prompt, output_file)
    
    print("\n" + "="*60)
    print(f"[SUCCESS] Created {len(test_prompts)} demo coloring pages!")
    print(f"          Check the '{output_dir}' folder")
    print("="*60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Use command line argument as prompt
        prompt = " ".join(sys.argv[1:])
        create_demo_coloring_page(prompt)
    else:
        # Run full test
        test_image_processing()
        
        print("\nTip: You can also run this with a custom prompt:")
        print("     python demo_generator.py A magical unicorn")

