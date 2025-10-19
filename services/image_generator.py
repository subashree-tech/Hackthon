import os
import io
import requests
import base64
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageEnhance
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
        """Generate base image using Stability AI API"""
        try:
            headers = {
                "Accept": "image/png",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "text_prompts": [
                    {
                        "text": f"{prompt}, black and white line art, coloring page style, simple lines, no shading",
                        "weight": 1.0
                    }
                ],
                "cfg_scale": Config.CFG_SCALE,
                "height": Config.IMAGE_HEIGHT,
                "width": Config.IMAGE_WIDTH,
                "samples": Config.SAMPLES,
                "steps": Config.STEPS,
                "style_preset": "line-art"
            }
            
            response = requests.post(
                f"{self.api_host}/v1/generation/{self.engine_id}/text-to-image",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if 'artifacts' in response_data and len(response_data['artifacts']) > 0:
                    image_data = response_data['artifacts'][0]['base64']
                    image_bytes = base64.b64decode(image_data)
                    return Image.open(io.BytesIO(image_bytes))
            
            print(f"API Error: {response.status_code} - {response.text}")
            return None
            
        except Exception as e:
            print(f"Error generating base image: {str(e)}")
            return None
    
    def _convert_to_coloring_page(self, image):
        """Convert image to coloring page style using PIL only"""
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Apply edge detection using PIL filters
            image = image.filter(ImageFilter.FIND_EDGES)
            
            # Invert colors (black lines on white background)
            image = ImageOps.invert(image)
            
            # Convert back to RGB for saving
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Make background white and lines black
            image = self._clean_coloring_page(image)
            
            return image
            
        except Exception as e:
            print(f"Error converting to coloring page: {str(e)}")
            return image
    
    def _clean_coloring_page(self, image):
        """Clean up the coloring page to ensure proper contrast"""
        try:
            # Convert to grayscale for processing
            gray = image.convert('L')
            
            # Create a new white image
            result = Image.new('RGB', image.size, 'white')
            
            # Get pixel data
            pixels = gray.load()
            result_pixels = result.load()
            
            width, height = image.size
            
            # Process each pixel
            for x in range(width):
                for y in range(height):
                    # If pixel is dark (likely a line), make it black
                    if pixels[x, y] < 128:  # Threshold for line detection
                        result_pixels[x, y] = (0, 0, 0)  # Black
                    else:
                        result_pixels[x, y] = (255, 255, 255)  # White
            
            return result
            
        except Exception as e:
            print(f"Error cleaning coloring page: {str(e)}")
            return image
    
    def add_fill_markers(self, image, marker_type='triangle', marker_size=8, min_area=500):
        """
        Add small markers to indicate fillable areas
        
        Args:
            image: PIL Image object
            marker_type: Type of marker ('triangle', 'circle', 'square')
            marker_size: Size of markers in pixels
            min_area: Minimum area to add a marker
            
        Returns:
            PIL Image with markers added
        """
        try:
            # Create a copy of the image
            result = image.copy()
            draw = ImageDraw.Draw(result)
            
            # Convert to grayscale for analysis
            gray = image.convert('L')
            pixels = gray.load()
            width, height = image.size
            
            # Find enclosed areas and add markers
            visited = set()
            areas = []
            
            for x in range(0, width, marker_size):
                for y in range(0, height, marker_size):
                    if (x, y) not in visited and pixels[x, y] > 200:  # White area
                        area_points = self._flood_fill_area(gray, x, y, visited, threshold=200)
                        if len(area_points) > min_area:
                            # Find center of area
                            center_x = sum(p[0] for p in area_points) // len(area_points)
                            center_y = sum(p[1] for p in area_points) // len(area_points)
                            areas.append((center_x, center_y, len(area_points)))
            
            # Add markers to largest areas
            areas.sort(key=lambda x: x[2], reverse=True)
            for i, (cx, cy, area_size) in enumerate(areas[:5]):  # Top 5 areas
                self._draw_marker(draw, cx, cy, marker_type, marker_size)
            
            return result
            
        except Exception as e:
            print(f"Error adding fill markers: {str(e)}")
            return image
    
    def _flood_fill_area(self, image, start_x, start_y, visited, threshold=200):
        """Simple flood fill to find connected white areas"""
        try:
            pixels = image.load()
            width, height = image.size
            area_points = []
            stack = [(start_x, start_y)]
            
            while stack:
                x, y = stack.pop()
                if (x, y) in visited or x < 0 or x >= width or y < 0 or y >= height:
                    continue
                
                if pixels[x, y] < threshold:
                    continue
                
                visited.add((x, y))
                area_points.append((x, y))
                
                # Add neighbors
                stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
            
            return area_points
            
        except Exception as e:
            print(f"Error in flood fill: {str(e)}")
            return []
    
    def _draw_marker(self, draw, x, y, marker_type, size):
        """Draw a marker at the specified position"""
        try:
            half_size = size // 2
            
            if marker_type == 'triangle':
                # Draw triangle
                points = [
                    (x, y - half_size),
                    (x - half_size, y + half_size),
                    (x + half_size, y + half_size)
                ]
                draw.polygon(points, fill='black')
                
            elif marker_type == 'circle':
                # Draw circle
                draw.ellipse([x - half_size, y - half_size, 
                            x + half_size, y + half_size], 
                           fill='black')
                
            elif marker_type == 'square':
                # Draw square
                draw.rectangle([x - half_size, y - half_size, 
                              x + half_size, y + half_size], 
                             fill='black')
                
        except Exception as e:
            print(f"Error drawing marker: {str(e)}")


# Example usage and testing
if __name__ == "__main__":
    generator = ImageGenerator()
    
    # Test with a simple prompt
    test_prompt = "A cute cat sitting"
    output_path = "test_coloring_page.png"
    
    success = generator.generate_coloring_page(test_prompt, output_path)
    if success:
        print(f"✅ Successfully generated coloring page: {output_path}")
    else:
        print("❌ Failed to generate coloring page")