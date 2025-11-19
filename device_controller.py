"""
Device Controller - UIAutomator2 Device Operations

Handles all physical device interactions:
- Screenshot capture
- UI hierarchy dump
- Click/tap actions
- Typing/input
- Scrolling/swiping
- Navigation (back, home, etc.)
"""

import time
import uiautomator2 as u2
from typing import Tuple, Optional
import re


class DeviceController:
    """Manages Android device operations via UIAutomator2."""
    
    def __init__(self):
        """Initialize device connection."""
        self.device = None
        self.screen_width = 1080
        self.screen_height = 2400
        self.screenshot_path = "current_screen.png"
        self.hierarchy_path = "current_hierarchy.xml"
        
        self._connect()
    
    def _connect(self):
        """Connect to Android device."""
        try:
            self.device = u2.connect()
            print(f"✅ Device connected: {self.device.info}")
            
            # Get actual screen dimensions
            window_size = self.device.window_size()
            self.screen_width = window_size[0]
            self.screen_height = window_size[1]
            print(f"📱 Screen: {self.screen_width}x{self.screen_height}")
            
        except Exception as e:
            print(f"❌ Device connection failed: {e}")
            raise
    
    # ==================== Screen Capture ====================
    
    def capture_screen(self, save_path: str) -> bool:
        """
        Capture current screen.
        
        Args:
            save_path: Path to save screenshot
            
        Returns:
            Success status
        """
        try:
            screenshot = self.device.screenshot()
            screenshot.save(save_path)
            print(f"📸 Screenshot: {save_path}")
            return True
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return False
    
    def dump_hierarchy(self) -> str:
        """
        Dump UI hierarchy XML.
        
        Returns:
            Path to saved XML file
        """
        try:
            xml_content = self.device.dump_hierarchy()
            with open(self.hierarchy_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            print(f"🌳 Hierarchy: {self.hierarchy_path}")
            return self.hierarchy_path
        except Exception as e:
            print(f"❌ Hierarchy dump failed: {e}")
            return None
    
    # ==================== Actions ====================
    
    def click(self, x: int, y: int) -> bool:
        """
        Click at pixel coordinates.
        
        Args:
            x: X coordinate in pixels
            y: Y coordinate in pixels
            
        Returns:
            Success status
        """
        try:
            self.device.click(x, y)
            print(f"👆 Clicked: ({x}, {y})")
            return True
        except Exception as e:
            print(f"❌ Click failed: {e}")
            return False
    
    def type_text(self, text: str) -> bool:
        """
        Type text into focused field.
        
        Args:
            text: Text to type
            
        Returns:
            Success status
        """
        try:
            self.device.send_keys(text)
            print(f"⌨️  Typed: {text}")
            return True
        except Exception as e:
            print(f"❌ Typing failed: {e}")
        return False
    
    def scroll(self, direction: str = "down") -> bool:
        """
        Scroll screen in direction.
        
        Args:
            direction: "up", "down", "left", "right"
            
        Returns:
            Success status
        """
        try:
            if direction == "down":
                self.device.swipe(
                    self.screen_width // 2, self.screen_height * 2 // 3,
                    self.screen_width // 2, self.screen_height // 3,
                    0.3
                )
            elif direction == "up":
                self.device.swipe(
                    self.screen_width // 2, self.screen_height // 3,
                    self.screen_width // 2, self.screen_height * 2 // 3,
                    0.3
                )
            elif direction == "left":
                self.device.swipe(
                    self.screen_width * 2 // 3, self.screen_height // 2,
                    self.screen_width // 3, self.screen_height // 2,
                    0.3
                )
            elif direction == "right":
                self.device.swipe(
                    self.screen_width // 3, self.screen_height // 2,
                    self.screen_width * 2 // 3, self.screen_height // 2,
                    0.3
                )
            
            print(f"📜 Scrolled: {direction}")
            return True
        except Exception as e:
            print(f"❌ Scroll failed: {e}")
            return False
    
    def swipe(self, direction: str) -> bool:
        """
        Swipe screen (same as scroll, for clarity).
        
        Args:
            direction: "left", "right", "up", "down"
            
        Returns:
            Success status
        """
        return self.scroll(direction)
    
    def press_key(self, key: str) -> bool:
        """
        Press device key.
        
        Args:
            key: "back", "home", "enter", etc.
            
        Returns:
            Success status
        """
        try:
            self.device.press(key)
            print(f"🔘 Pressed: {key}")
            return True
        except Exception as e:
            print(f"❌ Key press failed: {e}")
            return False
    
    # ==================== Utilities ====================
    
    def wait(self, seconds: float):
        """Wait for specified duration."""
        time.sleep(seconds)
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen dimensions."""
        return (self.screen_width, self.screen_height)
    
    def convert_normalized_to_pixels(self, x: float, y: float) -> Tuple[int, int]:
        """
        Convert normalized coordinates (0-1) to pixels.
        
        Args:
            x: Normalized x (0-1)
            y: Normalized y (0-1)
            
        Returns:
            (pixel_x, pixel_y)
        """
        pixel_x = int(x * self.screen_width)
        pixel_y = int(y * self.screen_height)
        return (pixel_x, pixel_y)
    
    def perform_action(self, step: str, pixel_coords: Optional[Tuple[int, int]] = None) -> bool:
        """
        Intelligently perform action based on step description.
        
        Args:
            step: Natural language step (e.g., "click search", "type hello", "scroll down")
            pixel_coords: Coordinates for click actions
            
        Returns:
            Success status
        """
        try:
            step_lower = step.lower()
            
            # Type/Input action
            if "type" in step_lower or "input" in step_lower or "enter" in step_lower:
                text = self._extract_text(step)
                if text:
                    return self.type_text(text)
                return False
            
            # Scroll/Swipe action
            elif "scroll" in step_lower or "swipe" in step_lower:
                direction = "down"  # default
                if "up" in step_lower:
                    direction = "up"
                elif "left" in step_lower:
                    direction = "left"
                elif "right" in step_lower:
                    direction = "right"
                return self.scroll(direction)
            
            # Back/Home key press
            elif "press" in step_lower or "back" in step_lower:
                if "back" in step_lower:
                    return self.press_key("back")
                elif "home" in step_lower:
                    return self.press_key("home")
                elif "enter" in step_lower:
                    return self.press_key("enter")
                return False
            
            # Wait action
            elif "wait" in step_lower:
                seconds = self._extract_wait_time(step)
                self.wait(seconds)
                print(f"⏳ Waited {seconds}s")
                return True
            
            # Default: Click action
            else:
                if pixel_coords:
                    x, y = pixel_coords
                    return self.click(x, y)
                return False
                
        except Exception as e:
            print(f"❌ Action failed: {e}")
            return False
    
    def _extract_text(self, step: str) -> Optional[str]:
        """Extract text to type from step."""
        step_lower = step.lower()
        keywords = ["type ", "input ", "enter ", "text "]
        
        for keyword in keywords:
            if keyword in step_lower:
                idx = step_lower.index(keyword) + len(keyword)
                text = step[idx:].strip()
                return text.replace(" and press enter", "").replace(" and send", "").strip()
        return None
    
    def _extract_wait_time(self, step: str) -> float:
        """Extract wait duration from step."""
        match = re.search(r'wait\s+(\d+)', step.lower())
        if match:
            return float(match.group(1))
        return 2.0  # default

