import os
import io
import requests
import base64
from PIL import Image, ImageFilter, ImageOps, ImageDraw
import cv2
import numpy as np
from config import Config


class ImageGenerator:
    """Handles image generation using Stability AI and conversion to coloring pages"""
    
    def __init__(self):
        self.api_key = Config.STABILITY_API_KEY
        self.api_host = Config.STABILITY_API_HOST
        self.engine_id = "stable-diffusion-xl-1024-v1-0"
        
    def generate_coloring_page(self, prompt, output_path, add_markers=True):
        """
        Generate a monochrome coloring page from a text prompt
        
        Args:
            prompt (str): Text description of what to draw
            output_path (str): Path where to save the output image
            add_markers (bool): Whether to add triangle markers to fillable areas
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Step 1: Generate base image using Stability AI
            base_image = self._generate_base_image(prompt)
            if base_image is None:
                return False
            
            # Step 2: Convert to coloring page style
            coloring_page = self._convert_to_coloring_page(base_image)
            
            # Step 3: Add fill markers if requested
            if add_markers:
                coloring_page = self.add_fill_markers(coloring_page, marker_type='triangle')
            
            # Step 4: Save the result
            coloring_page.save(output_path, 'PNG')
            print(f"Coloring page saved to: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"Error generating coloring page: {str(e)}")
            return False
    
    def _generate_base_image(self, prompt):
        """
        Generate base image using Stability AI API
        
        Args:
            prompt (str): Text description
            
        Returns:
            PIL.Image or None: Generated image or None if failed
        """
        if not self.api_key or self.api_key == 'your-stability-api-key-here' or self.api_key == 'demo-mode':
            print("Warning: No valid Stability API key found. Using fallback method.")
            print(f"API Key provided: {self.api_key[:10]}..." if self.api_key else "No API key")
            return self._generate_fallback_image(prompt)
        
        try:
            # Enhanced prompt for better coloring page generation
            enhanced_prompt = f"{prompt}, simple line art, black outline drawing, coloring book style, thick black lines, minimal details, child-friendly, cartoon style, clear shapes, easy to color, no shading, no gradients, outline only"
            
            url = f"{self.api_host}/v1/generation/{self.engine_id}/text-to-image"
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            body = {
                "text_prompts": [
                    {
                        "text": enhanced_prompt,
                        "weight": 1
                    },
                    {
                        "text": "blurry, complex details, realistic, photograph, photo, colored, gradient",
                        "weight": -1
                    }
                ],
                "cfg_scale": Config.CFG_SCALE,
                "height": Config.IMAGE_HEIGHT,
                "width": Config.IMAGE_WIDTH,
                "samples": Config.SAMPLES,
                "steps": Config.STEPS,
            }
            
            response = requests.post(url, headers=headers, json=body)
            
            if response.status_code != 200:
                print(f"Stability AI API error: {response.status_code} - {response.text}")
                print(f"Using engine: {self.engine_id}")
                print(f"API Host: {self.api_host}")
                return self._generate_fallback_image(prompt)
            
            data = response.json()
            
            # Decode the base64 image
            for artifact in data.get("artifacts", []):
                if artifact.get("finishReason") == "SUCCESS":
                    image_data = base64.b64decode(artifact["base64"])
                    image = Image.open(io.BytesIO(image_data))
                    return image
            
            return None
            
        except Exception as e:
            print(f"Error calling Stability AI API: {str(e)}")
            return self._generate_fallback_image(prompt)
    
    def _generate_fallback_image(self, prompt):
        """
        Generate a simple fallback image when API is not available
        This creates a basic placeholder that can still be converted to a coloring page
        
        Args:
            prompt (str): Text description
            
        Returns:
            PIL.Image: Simple generated image
        """
        # Create a white canvas
        img = Image.new('RGB', (Config.IMAGE_WIDTH, Config.IMAGE_HEIGHT), 'white')
        
        # Add some basic shapes based on keywords in the prompt
        # This is a very basic implementation - in production, you'd want the real API
        draw = ImageDraw.Draw(img)
        
        # Analyze prompt for different shapes
        prompt_lower = prompt.lower()
        
        # Draw different shapes based on keywords
        if any(word in prompt_lower for word in ['cat', 'dog', 'animal', 'pet']):
            # Draw animal shapes
            draw.ellipse([150, 150, 362, 362], outline='black', width=3)  # Head
            draw.ellipse([180, 200, 230, 250], outline='black', width=2)  # Eye
            draw.ellipse([282, 200, 332, 250], outline='black', width=2)  # Eye
            draw.arc([200, 250, 312, 330], 0, 180, fill='black', width=2)  # Smile
            draw.polygon([(256, 120), (220, 80), (292, 80)], outline='black', width=2)  # Ears
            
        elif any(word in prompt_lower for word in ['robot', 'machine']):
            # Draw robot shapes
            draw.rectangle([180, 180, 332, 380], outline='black', width=3)  # Body
            draw.rectangle([170, 150, 342, 200], outline='black', width=3)  # Head
            draw.ellipse([210, 165, 230, 185], outline='black', width=2)  # Eye
            draw.ellipse([282, 165, 302, 185], outline='black', width=2)  # Eye
            draw.rectangle([200, 300, 312, 350], outline='black', width=2)  # Control panel
            
        elif any(word in prompt_lower for word in ['flower', 'plant', 'tree']):
            # Draw flower shapes
            center_x, center_y = 256, 256
            draw.ellipse([center_x-30, center_y-30, center_x+30, center_y+30], outline='black', width=3)  # Center
            # Petals
            for angle in range(0, 360, 60):
                import math
                x = center_x + 60 * math.cos(math.radians(angle))
                y = center_y + 60 * math.sin(math.radians(angle))
                draw.ellipse([x-25, y-25, x+25, y+25], outline='black', width=2)
            # Stem
            draw.line([(center_x, center_y+30), (center_x, 400)], fill='black', width=3)
            
        elif any(word in prompt_lower for word in ['star', 'space', 'sky']):
            # Draw star shapes
            points = [(256, 150), (275, 210), (340, 210), (290, 250), 
                      (310, 315), (256, 280), (202, 315), (222, 250), 
                      (172, 210), (237, 210)]
            draw.polygon(points, outline='black', width=3)
            
        elif any(word in prompt_lower for word in ['dragon', 'monster']):
            # Draw dragon shapes
            draw.ellipse([150, 200, 362, 350], outline='black', width=3)  # Body
            draw.polygon([(256, 150), (200, 100), (312, 100)], outline='black', width=3)  # Head
            draw.ellipse([220, 120, 240, 140], outline='black', width=2)  # Eye
            draw.ellipse([272, 120, 292, 140], outline='black', width=2)  # Eye
            # Wings
            draw.ellipse([100, 220, 180, 300], outline='black', width=2)
            draw.ellipse([332, 220, 412, 300], outline='black', width=2)
            
        else:
            # Default shapes for unknown prompts
            draw.rectangle([50, 50, 462, 462], outline='black', width=3)
            draw.ellipse([150, 150, 362, 362], outline='black', width=3)
            draw.polygon([(256, 100), (200, 200), (312, 200)], outline='black', width=2)
        
        # Add text indicating this is a demo
        draw.text((256, 30), "Demo Mode", fill='black', anchor='mm')
        draw.text((256, 480), prompt[:40], fill='black', anchor='mm')
        
        return img
    
    def _convert_to_coloring_page(self, image):
        """
        Convert a regular image to a coloring page style
        (single bold black outlines on white background)
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            PIL.Image: Coloring page style image with single bold lines
        """
        # Convert PIL Image to numpy array for OpenCV processing
        img_array = np.array(image)
        
        # Convert to grayscale
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Apply moderate Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection - more sensitive to capture all important edges
        edges = cv2.Canny(
            blurred,
            threshold1=30,
            threshold2=90
        )
        
        # Dilate edges to make them thicker and more visible
        kernel_thick = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel_thick, iterations=2)
        
        # Close small gaps in the lines
        kernel_close = np.ones((3, 3), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel_close, iterations=1)
        
        # Remove very small noise (but keep main lines)
        # This removes tiny dots while preserving actual drawing lines
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(edges, connectivity=8)
        
        # Create output
        cleaned_edges = np.zeros_like(edges)
        
        # Much smaller threshold - only remove really tiny artifacts
        min_size = 20  # Very small threshold to keep most content
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] >= min_size:
                cleaned_edges[labels == i] = 255
        
        # Invert: black lines on white background
        coloring_page = cv2.bitwise_not(cleaned_edges)
        
        # Light median blur to smooth without losing detail
        coloring_page = cv2.medianBlur(coloring_page, 3)
        
        # Threshold to ensure pure black and white
        _, coloring_page = cv2.threshold(coloring_page, 240, 255, cv2.THRESH_BINARY)
        
        # Convert to PIL
        result = Image.fromarray(coloring_page)
        result = result.convert('L')
        
        # Enhance contrast
        result = ImageOps.autocontrast(result, cutoff=1)
        
        # Final conversion to pure black/white
        result = result.point(lambda x: 0 if x < 200 else 255, 'L')
        result = result.convert('RGB')
        
        return result
    
    def add_fill_markers(self, image, marker_type='triangle', marker_size=8):
        """
        Add small marker symbols to areas that should be filled
        Detects enclosed regions and adds markers to guide coloring
        
        Args:
            image (PIL.Image): Coloring page image
            marker_type (str): Type of marker ('circle', 'triangle', 'square')
            marker_size (int): Size of the marker in pixels
            
        Returns:
            PIL.Image: Image with markers added
        """
        # Convert to numpy array
        img_array = np.array(image.convert('L'))
        
        # Threshold to get binary image (black lines = 0, white background = 255)
        _, binary = cv2.threshold(img_array, 200, 255, cv2.THRESH_BINARY)
        
        # Invert so that lines are white (255) and regions are black (0)
        inverted = cv2.bitwise_not(binary)
        
        # Find contours - these represent the enclosed regions
        contours, hierarchy = cv2.findContours(
            inverted, 
            cv2.RETR_CCOMP,  # Get both outer and inner contours
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Convert back to PIL for drawing
        result = image.copy()
        draw = ImageDraw.Draw(result)
        
        # Parameters for filtering regions
        min_area = 300  # Minimum area to place a marker (avoid tiny regions)
        max_area = (image.width * image.height) * 0.8  # Avoid the background
        
        # Track placed markers to avoid overlap
        placed_markers = []
        min_distance = marker_size * 3  # Minimum distance between markers
        
        for i, contour in enumerate(contours):
            # Calculate area
            area = cv2.contourArea(contour)
            
            # Skip if too small or too large
            if area < min_area or area > max_area:
                continue
            
            # Get the center of the contour using moments
            M = cv2.moments(contour)
            if M['m00'] == 0:
                continue
                
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            
            # Check if point is inside the region (not on a line)
            # Sample a small area around the center point
            sample_size = 5
            x1 = max(0, cx - sample_size)
            x2 = min(binary.shape[1], cx + sample_size)
            y1 = max(0, cy - sample_size)
            y2 = min(binary.shape[0], cy + sample_size)
            
            sample_region = binary[y1:y2, x1:x2]
            if sample_region.size == 0 or np.mean(sample_region) < 200:
                continue  # Skip if on or near a line
            
            # Check distance from previously placed markers
            too_close = False
            for (px, py) in placed_markers:
                distance = np.sqrt((cx - px)**2 + (cy - py)**2)
                if distance < min_distance:
                    too_close = True
                    break
            
            if too_close:
                continue
            
            # Add marker at this location
            if marker_type == 'triangle':
                # Draw upward-pointing triangle
                half_size = marker_size // 2
                points = [
                    (cx, cy - half_size),  # Top
                    (cx - half_size, cy + half_size),  # Bottom left
                    (cx + half_size, cy + half_size)   # Bottom right
                ]
                draw.polygon(points, fill='black', outline='black')
                
            elif marker_type == 'circle':
                draw.ellipse(
                    [cx - marker_size//2, cy - marker_size//2, 
                     cx + marker_size//2, cy + marker_size//2],
                    fill='black', outline='black'
                )
                
            elif marker_type == 'square':
                draw.rectangle(
                    [cx - marker_size//2, cy - marker_size//2,
                     cx + marker_size//2, cy + marker_size//2],
                    fill='black', outline='black'
                )
            
            # Record this marker position
            placed_markers.append((cx, cy))
        
        return result