# Manava for Mobile 🤖📱

**Pure vision-based Android automation with Moondream AI**

Clean, production-ready architecture for intelligent mobile test automation.

---

## 🎯 What It Does

Executes natural language test cases on Android devices using:
- **Moondream** for screen reading and understanding
- **UIAutomator2** for device control and actions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     VisionAgent                         │
│                   (Orchestrator)                        │
└───────────┬──────────────────┬────────────┬────────────┘
            │                  │            │
    ┌───────▼────────┐  ┌─────▼──────┐  ┌──▼──────────┐
    │ ScreenParser   │  │  Device    │  │    Stats    │
    │  (Moondream)   │  │ Controller │  │  Tracker    │
    │                │  │(UIAutomator2)│  │             │
    │ • Vision       │  │ • Actions  │  │ • Metrics   │
    │ • Reasoning    │  │ • Clicks   │  │ • Analytics │
    │ • Location     │  │ • Typing   │  │             │
    └────────────────┘  └────────────┘  └─────────────┘
```

### Clean OOP Design
- **Composition over inheritance**
- **Single responsibility per module**
- **No code duplication**
- **Production-ready structure**

---

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Python 3.8+
python --version

# Android device via USB
adb devices
```

### 2. Install

```bash
pip install -r requirements.txt
```

### 3. Configure

Get your [Moondream API key](https://moondream.ai/) and update `main_vision.py`:

```python
MOONDREAM_API_KEY = "your_key_here"
```

### 4. Run

```bash
# Start API server
python main_vision.py

# Server runs at http://localhost:8001
```

---

## 📖 Usage

### Run Test Cases

**POST** `/run_test`

```json
{
  "app_name": "WhatsApp",
  "steps": [
    "click search icon",
    "type Hello World",
    "scroll down",
    "press back"
  ]
}
```

### Response

```json
{
  "status": "success",
  "completed_steps": 4,
  "total_steps": 4,
  "statistics": {
    "actions": {
      "total": 4,
      "successful": 4,
      "success_rate": 100.0
    },
    "api_calls": {
      "moondream_query": 2,
      "moondream_point": 4,
      "total": 6
    },
    "timing": {
      "duration_seconds": 12.5
    }
  }
}
```

### Other Endpoints

- **GET** `/` - API information
- **GET** `/health` - Agent status
- **GET** `/screen` - Current screenshot

---

## 🧩 Code Structure

```
manava/
├── vision_agent.py          # Main orchestrator
├── device_controller.py     # UIAutomator2 actions
├── screen_parser.py         # Moondream vision
├── stats_tracker.py         # Metrics tracking
├── main_vision.py           # FastAPI server
├── requirements.txt         # Dependencies
└── README.md               # You are here
```

### Module Responsibilities

| Module | Purpose | Key Methods |
|--------|---------|-------------|
| `VisionAgent` | Orchestration | `run_test_case()`, `_execute_step()` |
| `DeviceController` | Physical actions | `click()`, `type_text()`, `scroll()` |
| `ScreenParser` | Visual intelligence | `query()`, `locate()`, `check_visibility()` |
| `StatsTracker` | Analytics | `record_action()`, `get_summary()` |

---

## 🎨 Features

### ✨ Intelligent Mode

Automatically navigates to find elements:

1. **Visibility Check** - Moondream checks if element is visible
2. **Navigation Planning** - Suggests scroll/click/back
3. **Auto-Navigation** - Executes suggested action
4. **Retry** - Locates element after navigation

### 📊 Statistics Tracking

Detailed metrics:
- API calls (query/point/reasoning)
- Action success rates
- Detection sources (Moondream/UIAutomator)
- Auto-navigation counts
- Performance timing

### 🛡️ Robust Error Handling

- Automatic retries (3 attempts)
- Graceful degradation
- Detailed error logging
- Statistics on failures

---

## 🧪 Example Test Cases

### Simple Navigation
```json
{
  "app_name": "Settings",
  "steps": [
    "scroll down",
    "click display settings",
    "press back"
  ]
}
```

### Text Input
```json
{
  "app_name": "Notes",
  "steps": [
    "click new note button",
    "type Meeting notes for today",
    "click save button"
  ]
}
```

### Complex Flow
```json
{
  "app_name": "Instagram",
  "steps": [
    "click search icon",
    "type nature photography",
    "scroll down",
    "click first post",
    "click like button",
    "press back"
  ]
}
```

---

## 🔧 Advanced Usage

### Direct Agent Usage

```python
from vision_agent import VisionAgent

# Initialize
agent = VisionAgent(
    moondream_api_key="your_key",
    intelligent_mode=True
)

# Run test
result = agent.run_test_case({
    "app_name": "My App",
    "steps": ["click button", "type text"]
})

# Query screen
answer = agent.query_screen("What app is open?")

# Get statistics
stats = agent.get_statistics()
```

### Custom Actions

The `DeviceController` intelligently parses natural language:

- **Click**: `"click search icon"`, `"tap settings button"`
- **Type**: `"type hello world"`, `"enter user@email.com"`
- **Scroll**: `"scroll down"`, `"swipe up"`, `"scroll left"`
- **Press**: `"press back"`, `"press home"`, `"press enter"`
- **Wait**: `"wait 3 seconds"`

---

## 🎯 Why This Architecture?

### Before (Monolithic)
- ❌ 1100+ line single file
- ❌ Mixed responsibilities
- ❌ Hard to test
- ❌ Code duplication

### After (Clean OOP)
- ✅ 4 focused modules (~300 lines each)
- ✅ Single responsibility
- ✅ Easy to test
- ✅ No duplication
- ✅ Production-ready

---

## 📦 Dependencies

```
fastapi         # REST API server
uvicorn         # ASGI server
pydantic        # Data validation
uiautomator2    # Android automation
pillow          # Image processing
```

No heavy dependencies. No LLM needed. Pure vision intelligence.

---

## 🤝 Contributing

This is a production-ready, clean architecture. When extending:

1. **Maintain single responsibility** - One module, one job
2. **Use composition** - Not inheritance
3. **Keep it DRY** - No code duplication
4. **Test thoroughly** - Verify changes work
5. **Document clearly** - Explain your additions

---

## 📄 License

MIT License - Use freely for any purpose.

---

## 🙏 Credits

- **Moondream AI** - Vision intelligence
- **UIAutomator2** - Android automation
- **FastAPI** - Modern Python web framework

---

**Built with ❤️ for intelligent mobile automation**

*Pure vision. Clean code. Production ready.*
