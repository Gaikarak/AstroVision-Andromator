"""
Screen Parser - Moondream Vision Intelligence

Handles all visual understanding:
- Screen analysis
- Element detection
- Location finding
- Visual reasoning
"""

import base64
import json
import urllib.request
from typing import Optional, Dict
from PIL import Image
import io
from stats_tracker import StatsTracker


class ScreenParser:
    """Manages visual understanding via Moondream."""
    
    def __init__(self, api_key: str, stats: Optional[StatsTracker] = None):
        """
        Initialize screen parser.
        
        Args:
            api_key: Moondream API key
            stats: Optional stats tracker
        """
        self.api_key = api_key
        self.query_url = "https://api.moondream.ai/v1/query"
        self.point_url = "https://api.moondream.ai/v1/point"
        self.stats = stats or StatsTracker()
    
    # ==================== Vision Intelligence ====================
    
    def query(self, image_path: str, question: str, retry: int = 1) -> Optional[str]:
        """
        Ask Moondream a question about the screen.
        
        Uses /v1/query endpoint for:
        - Visibility checks
        - Navigation suggestions
        - Validation
        - General reasoning
        
        Args:
            image_path: Path to screenshot
            question: Question to ask
            retry: Retry attempt number
            
        Returns:
            Answer string or None
        """
        try:
            # Optimize image
            encoded_image = self._optimize_image(image_path)
            
            # Build request
            payload = {
                "image": encoded_image,
                "question": question
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Make request
            req = urllib.request.Request(
                self.query_url,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            # Record stats
            self.stats.record_query_call()
            
            # Execute
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode('utf-8'))
                answer = result.get('answer', '')
                return answer
            
        except Exception as e:
            print(f"❌ Moondream query error (attempt {retry}): {e}")
            
            if retry < 3:
                import time
                time.sleep(1)
                return self.query(image_path, question, retry + 1)
            
            return None
    
    def locate(self, image_path: str, element_description: str, retry: int = 1) -> Optional[Dict]:
        """
        Locate element and get coordinates.
        
        Uses /v1/point endpoint for:
        - Finding element location
        - Getting normalized coordinates
        
        Args:
            image_path: Path to screenshot
            element_description: What to locate
            retry: Retry attempt number
            
        Returns:
            Dict with {'x': float, 'y': float} or None
        """
        try:
            # Optimize image
            encoded_image = self._optimize_image(image_path)
            
            # Build request
            payload = {
                "image": encoded_image,
                "object": element_description
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Make request
            req = urllib.request.Request(
                self.point_url,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            # Record stats
            self.stats.record_point_call()
            self.stats.record_detection("moondream")
            
            # Execute
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # Moondream returns [x, y] array
                if 'point' in result and isinstance(result['point'], list) and len(result['point']) == 2:
                    x, y = result['point']
                    print(f"✅ Moondream located: '{element_description}' at ({x:.3f}, {y:.3f})")
                    return {"x": x, "y": y}
                
                return None
            
        except Exception as e:
            print(f"❌ Moondream locate error (attempt {retry}): {e}")
            
            if retry < 3:
                import time
                time.sleep(1)
                return self.locate(image_path, element_description, retry + 1)
            
            return None
    
    def check_visibility(self, image_path: str, element_name: str) -> bool:
        """
        Check if element is visible on screen.
        
        Args:
            image_path: Path to screenshot
            element_name: Element to check
            
        Returns:
            True if visible
        """
        question = f"Is the {element_name} visible on this screen? Answer only 'yes' or 'no'."
        answer = self.query(image_path, question)
        
        if answer:
            self.stats.record_reasoning_call()
            return "yes" in answer.lower()
        
        return False
    
    def get_navigation_suggestion(self, image_path: str, goal: str) -> Optional[str]:
        """
        Get navigation suggestion from Moondream.
        
        Args:
            image_path: Path to screenshot
            goal: What element to find
            
        Returns:
            Navigation action (e.g., "scroll down", "click settings", "press back")
        """
        question = f"""
        I'm trying to find '{goal}' but it's not visible.
        
        Looking at this screen, what single action should I take?
        Respond with ONLY ONE action from these options:
        - "scroll down"
        - "scroll up"
        - "press back"
        - "click [specific element name]"
        - "not possible"
        
        Answer with just the action, nothing else.
        """
        
        answer = self.query(image_path, question)
        
        if answer:
            self.stats.record_reasoning_call()
            action = answer.strip().lower()
            
            # Validate action
            if any(cmd in action for cmd in ["scroll", "click", "press", "swipe", "not possible"]):
                return action
        
        return None
    
    def validate_action(self, image_path: str, expectation: str) -> bool:
        """
        Validate that action had expected result.
        
        Args:
            image_path: Path to screenshot (after action)
            expectation: What to check
            
        Returns:
            True if validation passed
        """
        question = f"Looking at this screen: {expectation}? Answer only 'yes' or 'no'."
        answer = self.query(image_path, question)
        
        if answer:
            return "yes" in answer.lower()
        
        return False
    
    # ==================== Helper Methods ====================
    
    def _optimize_image(self, image_path: str) -> str:
        """
        Optimize image for API (resize + JPEG).
        
        Args:
            image_path: Path to image
            
        Returns:
            Base64 encoded optimized image
        """
        img = Image.open(image_path)
        
        # Convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if large (max 1080px width)
        if img.width > 1080:
            ratio = 1080 / img.width
            new_height = int(img.height * ratio)
            img = img.resize((1080, new_height), Image.Resampling.LANCZOS)
        
        # Save as JPEG
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        
        # Encode to base64
        encoded = base64.b64encode(buffer.read()).decode('utf-8')
        return encoded
