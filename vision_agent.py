"""
Vision Agent - Intelligent Android Automation Orchestrator

Orchestrates:
1. DeviceController (UIAutomator2) - Physical actions
2. ScreenParser (Moondream) - Visual intelligence
3. StatsTracker - Metrics & analytics

Architecture:
- Pure composition (no inheritance)
- Single responsibility per component
- Clean separation of concerns
"""

from typing import Dict, Optional
import time

from device_controller import DeviceController
from screen_parser import ScreenParser
from stats_tracker import StatsTracker


class VisionAgent:
    """
    Intelligent Android Automation Agent.
    
    Pure Moondream Vision Intelligence:
    1. PERCEPTION: Moondream sees the screen
    2. REASONING: Moondream decides what to do
    3. LOCATION: Moondream finds elements
    4. ACTION: UIAutomator2 performs actions
    """
    
    def __init__(self, moondream_api_key: str, intelligent_mode: bool = True):
        """
        Initialize agent with clean composition.
        
        Args:
            moondream_api_key: Moondream API key
            intelligent_mode: Enable auto-navigation and reasoning
        """
        self.intelligent_mode = intelligent_mode
        self.screenshot_path = "current_screen.png"
        
        # Initialize components (composition, not inheritance!)
        print(f"\n🚀 Initializing Manava for Mobile...")
        print(f"🧠 Intelligent mode: {'ENABLED' if intelligent_mode else 'DISABLED'}\n")
        
        self.device = DeviceController()
        self.stats = StatsTracker()
        self.vision = ScreenParser(moondream_api_key, self.stats)
        
        print(f"✅ All systems ready!\n")
    
    # ==================== Core Workflow ====================
    
    def run_test_case(self, test_json: Dict) -> Dict:
        """
        Execute test case from JSON.
        
        Args:
            test_json: {
                "app_name": str,
                "steps": [str]  # Natural language steps
            }
            
        Returns:
            {
                "status": "success" | "failed",
                "completed_steps": int,
                "total_steps": int,
                "failed_step": str | None,
                "statistics": Dict
            }
        """
        app_name = test_json.get("app_name", "Test")
        steps = test_json.get("steps", [])
        
        print(f"\n{'='*80}")
        print(f"🎬 Starting Test: {app_name}")
        print(f"📝 Total Steps: {len(steps)}")
        print(f"{'='*80}\n")
        
        self.stats.start_test()
        completed_steps = 0
        failed_step = None
        
        try:
            for idx, step in enumerate(steps, 1):
                print(f"\n--- Step {idx}/{len(steps)}: {step} ---")
                
                # Execute step
                success = self._execute_step(step)
                
                if success:
                    completed_steps += 1
                    print(f"✅ Step {idx} completed")
                else:
                    failed_step = step
                    print(f"❌ Step {idx} failed")
                    break
                
                # Brief pause between steps
                time.sleep(0.5)
        
        finally:
            self.stats.end_test()
        
        # Generate result
        status = "success" if completed_steps == len(steps) else "failed"
        
        # Print summary
        self.stats.print_summary(app_name)
        
        return {
            "status": status,
            "completed_steps": completed_steps,
            "total_steps": len(steps),
            "failed_step": failed_step,
            "statistics": self.stats.get_summary()
        }
    
    def _execute_step(self, step: str) -> bool:
        """
        Execute a single step.
        
        Flow:
        1. Capture screen
        2. Locate element (with optional auto-navigation)
        3. Perform action
        4. Record result
        
        Args:
            step: Natural language step
            
        Returns:
            Success status
        """
        try:
            # 1. Capture screen
            print("📸 Capturing screen...")
            if not self.device.capture_screen(self.screenshot_path):
                print("❌ Failed to capture screen")
                return False
            
            # 2. Locate element
            coords = None
            
            # Check if this is a non-visual action (scroll, back, wait)
            step_lower = step.lower()
            if any(cmd in step_lower for cmd in ["scroll", "swipe", "back", "home", "wait"]):
                # Direct action, no location needed
                pass
            else:
                # Need to locate element
                if self.intelligent_mode:
                    coords = self._intelligent_locate(step)
                else:
                    coords = self._basic_locate(step)
                
                if coords is None and "type" not in step_lower:
                    print(f"❌ Could not locate element for: {step}")
                    self.stats.record_action(False)
                    return False
            
            # 3. Perform action
            pixel_coords = None
            if coords:
                pixel_coords = self.device.convert_normalized_to_pixels(coords['x'], coords['y'])
            
            success = self.device.perform_action(step, pixel_coords)
            
            # 4. Record result
            self.stats.record_action(success)
            
            return success
            
        except Exception as e:
            print(f"❌ Step execution error: {e}")
            self.stats.record_action(False)
            return False
    
    # ==================== Element Location Strategies ====================
    
    def _basic_locate(self, step: str) -> Optional[Dict]:
        """
        Basic location: Direct Moondream lookup.
        
        Args:
            step: Step description
            
        Returns:
            {'x': float, 'y': float} or None
        """
        print("🔍 Locating element...")
        return self.vision.locate(self.screenshot_path, step)
    
    def _intelligent_locate(self, step: str, max_retries: int = 3) -> Optional[Dict]:
        """
        Intelligent location with auto-navigation.
        
        Flow:
        1. Check if element visible
        2. If not visible → Ask Moondream for navigation
        3. Execute navigation action
        4. Retry location
        5. Repeat up to max_retries
        
        Args:
            step: Step description
            max_retries: Maximum navigation attempts
            
        Returns:
            {'x': float, 'y': float} or None
        """
        print("🔍 Intelligent locate (with auto-navigation)...")
        
        for attempt in range(max_retries):
            # Try to locate
            coords = self.vision.locate(self.screenshot_path, step)
            
            if coords:
                return coords
            
            # If not found and not last attempt
            if attempt < max_retries - 1:
                print(f"🤔 Element not found (attempt {attempt + 1}/{max_retries})")
                print("🧠 Asking Moondream for navigation advice...")
                
                # Get navigation suggestion
                action = self.vision.get_navigation_suggestion(self.screenshot_path, step)
                
                if action and "not possible" not in action:
                    print(f"💡 Moondream suggests: {action}")
                    self.stats.record_navigation()
                    
                    # Execute navigation
                    if self.device.perform_action(action):
                        print("✅ Navigation executed")
                        time.sleep(1)  # Wait for UI to settle
                        
                        # Recapture screen
                        self.device.capture_screen(self.screenshot_path)
                    else:
                        print("❌ Navigation failed")
                else:
                    print("❌ Moondream says navigation not possible")
                    break
        
        return None
    
    # ==================== Helper Methods ====================
    
    def get_statistics(self) -> Dict:
        """Get current statistics."""
        return self.stats.get_summary()
    
    def get_current_screen(self) -> str:
        """
        Get current screenshot path.
        
        Returns:
            Path to latest screenshot
        """
        self.device.capture_screen(self.screenshot_path)
        return self.screenshot_path
    
    def query_screen(self, question: str) -> Optional[str]:
        """
        Ask Moondream a question about current screen.
        
        Args:
            question: Question to ask
            
        Returns:
            Answer string
        """
        self.device.capture_screen(self.screenshot_path)
        return self.vision.query(self.screenshot_path, question)
    
    def validate_screen(self, expectation: str) -> bool:
        """
        Validate current screen state.
        
        Args:
            expectation: What to check
            
        Returns:
            True if validation passed
        """
        self.device.capture_screen(self.screenshot_path)
        return self.vision.validate_action(self.screenshot_path, expectation)


# ==================== Quick Testing ====================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                         MANAVA FOR MOBILE v5.0                               ║
    ║                     Pure Vision-Based Android Automation                     ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    
    Architecture:
    ✓ DeviceController (UIAutomator2) - Physical actions
    ✓ ScreenParser (Moondream) - Visual intelligence  
    ✓ StatsTracker - Metrics & analytics
    ✓ VisionAgent - Orchestration
    
    Clean Code:
    ✓ Single responsibility per component
    ✓ Pure composition (no inheritance)
    ✓ No code duplication
    ✓ Production-ready structure
    """)
    
    # Example usage
    MOONDREAM_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI2MDc3NzE3NS1iM2Q1LTRkMGQtYjNlYy00M2M4YWVhOWEyYTQiLCJvcmdfaWQiOiIyeGJvSHdPSFhidEtneWZTZkM3RDB5ZUd0U1ZtaGFEMiIsImlhdCI6MTc2MzQ1MDEyMCwidmVyIjoxfQ.WLPh0gCqGFn2qqqDd4oMcJH6KcfEsbwRGDS4sMGzPek"
    
    agent = VisionAgent(moondream_api_key=MOONDREAM_API_KEY, intelligent_mode=True)
    
    print("\n✅ Agent ready for testing!")
    print("\nRun with FastAPI:")
    print("  python main_vision.py")
    print("\nOr test directly:")
    print("  python test_intelligent_moondream.py")

