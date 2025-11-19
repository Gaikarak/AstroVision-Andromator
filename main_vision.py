"""FastAPI Server for Pure Moondream Vision Intelligence."""

import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vision_agent import VisionAgent

# ==================== Configuration ====================

MOONDREAM_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI2MDc3NzE3NS1iM2Q1LTRkMGQtYjNlYy00M2M4YWVhOWEyYTQiLCJvcmdfaWQiOiIyeGJvSHdPSFhidEtneWZTZkM3RDB5ZUd0U1ZtaGFEMiIsImlhdCI6MTc2MzQ1MDEyMCwidmVyIjoxfQ.WLPh0gCqGFn2qqqDd4oMcJH6KcfEsbwRGDS4sMGzPek"
INTELLIGENT_MODE = True  # Enable intelligent features (Moondream reasoning)

# ==================== FastAPI App ====================

app = FastAPI(
    title="Manava for Mobile",
    description="Pure vision-based automation: Moondream for 100% screen parsing, UIAutomator2 for actions only",
    version="5.0.0"
)

# Initialize Vision Agent
try:
    agent = VisionAgent(
        moondream_api_key=MOONDREAM_API_KEY,
        intelligent_mode=INTELLIGENT_MODE
    )
    print("✅ Vision Agent initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize Vision Agent: {e}")
    agent = None

# ==================== API Schemas ====================

class TestRequest(BaseModel):
    app_name: Optional[str] = "Unknown App"
    steps: List[str]
    execute: bool = True

# ==================== Endpoints ====================

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Pure Moondream Vision Intelligence API",
        "version": "5.0.0",
        "architecture": {
            "approach": "Pure Vision Intelligence",
            "perception": "Moondream /v1/query (sees and understands screen)",
            "reasoning": "Moondream /v1/query (decides navigation based on what it sees)",
            "location": "Moondream /v1/point (finds element coordinates)",
            "actions": "UIAutomator2 (clicks, swipes, typing)",
            "flow": "screenshot → Moondream analyzes → navigates if needed → locates → action"
        },
        "advantages": {
            "single_api": "One API sees everything - no blind LLM guessing",
            "visual_reasoning": "Moondream SEES the screen when making decisions",
            "auto_navigation": "Automatically finds elements even if not visible",
            "accurate": "Vision-based reasoning > text-based guessing",
            "simpler": "Pure Moondream - no extra LLM needed",
            "cheaper": "Single API, fewer calls"
        },
        "agent_status": "ready" if agent else "not initialized",
        "endpoints": {
            "POST /run_test": "Execute test case with natural language steps",
            "GET /health": "Check agent status",
            "GET /screen": "Get current screenshot",
            "POST /query_screen": "Query screen with custom question"
        }
    }

@app.get("/health")
def health_check():
    """Check if agent is ready."""
    if not agent:
        raise HTTPException(status_code=503, detail="Vision Agent not initialized")
    
    return {
        "status": "healthy",
        "agent": "ready",
        "device_connected": agent.device is not None,
        "screen_size": f"{agent.screen_width}x{agent.screen_height}"
    }

@app.get("/screen")
def get_current_screen():
    """Capture and return current screen info."""
    if not agent:
        raise HTTPException(status_code=503, detail="Vision Agent not initialized")
    
    try:
        screenshot_path = agent.capture_screen()
        return {
            "success": True,
            "screenshot_path": screenshot_path,
            "screen_size": {
                "width": agent.screen_width,
                "height": agent.screen_height
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to capture screen: {str(e)}")

@app.get("/parse_screen_llm")
def parse_screen_for_llm():
    """
    Parse screen into structured JSON optimized for LLM consumption.
    
    Returns organized data with:
    - app_context: App name, screen type, purpose
    - interactive_elements: Structured list of clickable/typeable elements
    - visible_content: Key text visible on screen
    - metadata: Technical info
    
    Perfect for sending to GPT-4, Claude, or other LLMs to decide actions.
    """
    if not agent:
        raise HTTPException(status_code=503, detail="Vision Agent not initialized")
    
    try:
        # Capture current screen
        agent.capture_screen()
        
        # Parse with Moondream
        result = agent.parse_screen_for_llm()
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Screen parsing failed"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse screen: {str(e)}")

@app.post("/run_test")
def run_test(request: TestRequest):
    """
    Execute a test case with natural language steps.
    
    Example:
    {
        "app_name": "Snapchat",
        "steps": [
            "click camera button",
            "take a photo",
            "click send button",
            "select friend john",
            "click send"
        ],
        "execute": true
    }
    """
    if not agent:
        raise HTTPException(status_code=503, detail="Vision Agent not initialized")
    
    if not request.steps:
        raise HTTPException(status_code=400, detail="At least one step is required")
    
    try:
        # Convert request to dict
        test_case = {
            "app_name": request.app_name,
            "steps": request.steps,
            "execute": request.execute
        }
        
        # Run test
        result = agent.run_test_case(test_case)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test execution failed: {str(e)}")

@app.post("/query_screen")
def query_screen(question: str):
    """
    Ask Moondream a question about the current screen.
    
    Example: "What app is currently open?" or "Is there a camera button visible?"
    """
    if not agent:
        raise HTTPException(status_code=503, detail="Vision Agent not initialized")
    
    try:
        # Capture screen
        screenshot_path = agent.capture_screen()
        
        # Query Moondream
        result = agent.query_moondream(screenshot_path, question)
        
        if result.get("success"):
            return {
                "success": True,
                "question": question,
                "answer": result["answer"]
            }
        else:
            return {
                "success": False,
                "question": question,
                "error": result.get("error", "Unknown error")
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

# ==================== Main ====================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*80)
    print("Manava for Mobile Vision-Based Automation")
    print("="*80)
    if INTELLIGENT_MODE:
        print("\n🧠 Mode: INTELLIGENT (Pure Moondream Vision)")
    else:
        print("\n🔮 Mode: BASIC (Simple element location only)")
    print("\n🌐 Starting server at http://localhost:8001")
    print("📖 API docs at http://localhost:8001/docs")
    print("\n" + "="*80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)

