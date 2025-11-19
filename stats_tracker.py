"""
Statistics Tracker - Centralized metrics and analytics

Tracks all automation statistics:
- API calls (Moondream query/point)
- Actions performed
- Success/failure rates
- Performance metrics
"""

from typing import Dict
import time


class StatsTracker:
    """Clean, centralized statistics management."""
    
    def __init__(self):
        """Initialize statistics trackers."""
        # API call tracking
        self.moondream_query_calls = 0
        self.moondream_point_calls = 0
        self.moondream_reasoning_calls = 0
        
        # Action tracking
        self.actions_performed = 0
        self.successful_actions = 0
        self.failed_actions = 0
        
        # Navigation tracking
        self.auto_navigations = 0
        
        # Element detection tracking
        self.moondream_detections = 0
        self.uiautomator_detections = 0
        
        # Timing
        self.start_time = None
        self.end_time = None
    
    # ==================== Recording Methods ====================
    
    def start_test(self):
        """Mark test start time."""
        self.start_time = time.time()
    
    def end_test(self):
        """Mark test end time."""
        self.end_time = time.time()
    
    def record_query_call(self):
        """Record Moondream /v1/query call."""
        self.moondream_query_calls += 1
    
    def record_point_call(self):
        """Record Moondream /v1/point call."""
        self.moondream_point_calls += 1
    
    def record_reasoning_call(self):
        """Record Moondream reasoning/navigation call."""
        self.moondream_reasoning_calls += 1
    
    def record_action(self, success: bool):
        """
        Record action execution.
        
        Args:
            success: Whether action succeeded
        """
        self.actions_performed += 1
        if success:
            self.successful_actions += 1
        else:
            self.failed_actions += 1
    
    def record_navigation(self):
        """Record auto-navigation attempt."""
        self.auto_navigations += 1
    
    def record_detection(self, source: str):
        """
        Record element detection.
        
        Args:
            source: "moondream" or "uiautomator"
        """
        if source == "moondream":
            self.moondream_detections += 1
        elif source == "uiautomator":
            self.uiautomator_detections += 1
    
    # ==================== Summary Methods ====================
    
    def get_duration(self) -> float:
        """Get test duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    def get_success_rate(self) -> float:
        """Get action success rate percentage."""
        if self.actions_performed == 0:
            return 0.0
        return (self.successful_actions / self.actions_performed) * 100
    
    def get_total_api_calls(self) -> int:
        """Get total Moondream API calls."""
        return self.moondream_query_calls + self.moondream_point_calls
    
    def get_total_detections(self) -> int:
        """Get total element detections."""
        return self.moondream_detections + self.uiautomator_detections
    
    def get_summary(self) -> Dict:
        """
        Get complete statistics summary.
        
        Returns:
            Dict with all statistics
        """
        total_detections = self.get_total_detections()
        
        return {
            "actions": {
                "total": self.actions_performed,
                "successful": self.successful_actions,
                "failed": self.failed_actions,
                "success_rate": round(self.get_success_rate(), 2)
            },
            "api_calls": {
                "moondream_query": self.moondream_query_calls,
                "moondream_point": self.moondream_point_calls,
                "moondream_reasoning": self.moondream_reasoning_calls,
                "total": self.get_total_api_calls()
            },
            "detection": {
                "moondream": self.moondream_detections,
                "uiautomator": self.uiautomator_detections,
                "total": total_detections,
                "moondream_percentage": round((self.moondream_detections / total_detections * 100), 1) if total_detections > 0 else 0
            },
            "navigation": {
                "auto_navigations": self.auto_navigations
            },
            "timing": {
                "duration_seconds": round(self.get_duration(), 2)
            }
        }
    
    def print_summary(self, app_name: str = "Test"):
        """
        Print formatted statistics summary.
        
        Args:
            app_name: Name of the app being tested
        """
        print(f"\n{'='*80}")
        print(f"🏁 Test Complete: {app_name}")
        print(f"✅ Successful: {self.successful_actions}/{self.actions_performed} ({self.get_success_rate():.1f}%)")
        print(f"❌ Failed: {self.failed_actions}")
        
        total_detections = self.get_total_detections()
        if total_detections > 0:
            print(f"\n📊 Element Detection:")
            print(f"   🔮 Moondream: {self.moondream_detections}/{total_detections} ({self.moondream_detections/total_detections*100:.1f}%)")
            print(f"   🤖 UIAutomator2: {self.uiautomator_detections}/{total_detections} ({self.uiautomator_detections/total_detections*100:.1f}%)")
        
        if self.moondream_reasoning_calls > 0 or self.auto_navigations > 0:
            print(f"\n🧠 Intelligence:")
            print(f"   💭 Reasoning Calls: {self.moondream_reasoning_calls}")
            print(f"   🔄 Auto-Navigations: {self.auto_navigations}")
            print(f"   📡 Total API Calls: {self.get_total_api_calls()}")
        
        if self.get_duration() > 0:
            print(f"\n⏱️  Duration: {self.get_duration():.1f}s")
        
        print(f"{'='*80}\n")
    
    def reset(self):
        """Reset all statistics."""
        self.__init__()

