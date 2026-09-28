# Smart Customer Support Chatbot - Local Setup & Run Guide

## ✅ Step 1: Clone or Navigate to Project

```bash
cd smart-customer-support-chatbot
```

---

## ✅ Step 2: Create Virtual Environment

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### On Windows (PowerShell):
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### On Windows (Command Prompt):
```bash
python -m venv venv
venv\Scripts\activate.bat
```

**Expected output:** You should see `(venv)` prefix in your terminal.

---

## ✅ Step 3: Upgrade pip, setuptools, and wheel

```bash
pip install --upgrade pip setuptools wheel
```

**Expected output:**
```
Successfully installed pip-X.X.X setuptools-X.X.X wheel-X.X.X
```

---

## ✅ Step 4: Install Project Dependencies

```bash
pip install -r requirements.txt
```

**This will take 5-10 minutes.** You should see:
```
Successfully installed <package-name> <package-name> ... (X packages in X.XXs)
```

### If Installation Fails:

**Option A: Install dependencies one at a time (safer):**
```bash
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install python-dotenv==1.0.0
pip install pydantic==2.5.0
pip install pydantic-settings==2.2.1
pip install sqlalchemy==2.0.23
pip install sentence-transformers==2.2.2
pip install numpy==1.24.3
```

**Option B: Use pre-built wheels (if torch fails):**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

---

## ✅ Step 5: Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

**Expected output:**
```
✓ Download and installation successful
You can now load the model via spacy.load('en_core_web_sm')
```

---

## ✅ Step 6: Create Environment File

```bash
cp .env.example .env
```

**On Windows:**
```bash
copy .env.example .env
```

The `.env` file now contains all configuration with safe defaults. No changes needed unless you want to customize.

---

## ✅ Step 7: Verify Project Structure

```bash
# List backend files
ls backend/

# List frontend files
ls frontend/

# List data files
ls data/
```

**You should see:**
```
backend/
├── __init__.py
├── main.py
├── config.py
├── database.py
├── models.py
├── pipeline.py
├── agent.py
├── schemas.py
├── websocket_handler.py
└── utils.py

frontend/
├── index.html
├── style.css
└── chat.js

data/
├── intents.json
└── faq.json
```

---

## ✅ Step 8: Start the Backend Server

```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Keep this terminal window open!** Do not close it.

### Common Startup Issues & Fixes:

**Issue: `ModuleNotFoundError: No module named 'backend'`**
```bash
# Make sure you're in the project root directory
pwd  # or 'cd' on Windows
# Should show: .../smart-customer-support-chatbot
```

**Issue: `Port 8000 already in use`**
```bash
# Use a different port
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
```

---

## ✅ Step 9: Test Health Endpoint (New Terminal Tab/Window)

**Open a NEW terminal window** (keep backend running in original)

```bash
curl http://localhost:8000/health
```

**Expected output:**
```json
{"status":"ok","timestamp":"2026-09-28T16:30:00.123456"}
```

---

## ✅ Step 10: Test Chat API Endpoint

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-1",
    "message": "I cannot login to my account",
    "user_id": "guest-user"
  }'
```

**Expected output:**
```json
{
  "session_id": "test-session-1",
  "response": "To fix login issues, please try the following...",
  "intent": "account_access",
  "confidence": 0.85,
  "escalated": false,
  "escalation_reason": null,
  "timestamp": "2026-09-28T16:30:15.123456"
}
```

### Try More Test Messages:

**Test 2 - Billing Issue:**
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-2",
    "message": "I was charged twice",
    "user_id": "guest-user"
  }'
```

**Test 3 - Technical Issue:**
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-3",
    "message": "The app keeps crashing",
    "user_id": "guest-user"
  }'
```

---

## ✅ Step 11: Open Frontend in Browser

### Option A: Direct File (May have CORS issues)
```bash
# Open in your browser
open frontend/index.html  # macOS
xdg-open frontend/index.html  # Linux
start frontend\index.html  # Windows
```

### Option B: Use Local HTTP Server (Recommended)

**In a NEW terminal tab:**

```bash
# Navigate to project root
cd smart-customer-support-chatbot

# Start HTTP server
python -m http.server 8080
```

**Expected output:**
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/)
```

Then open in your browser:
```
http://localhost:8080/frontend/index.html
```

---

## ✅ Step 12: Test Chat UI

1. **Type in the chat box:** `I cannot login to my account`
2. **Click Send** or press Enter
3. **Expected response:** Account access help text with FAQ answer
4. **Check bottom status:** Should show intent, confidence, and whether escalated

### Test Different Scenarios:

| Message | Expected Intent | Expected Action |
|---------|-----------------|-----------------|
| `I cannot login` | account_access | Direct answer |
| `I was charged twice` | billing_issue | Escalate (complex) |
| `App keeps crashing` | technical_issue | Escalate (complex) |
| `How do I upgrade?` | subscription | Direct answer or clarify |
| `Random text xyz` | unknown | Clarifying questions |

---

## 🎯 Running Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] spaCy model downloaded
- [ ] `.env` file created from `.env.example`
- [ ] Backend started (`uvicorn` running on port 8000)
- [ ] `/health` endpoint responds with OK
- [ ] `/api/chat/message` endpoint responds with valid JSON
- [ ] Frontend opens in browser at `http://localhost:8080/frontend/index.html`
- [ ] Chat sends message and receives response
- [ ] Response includes intent classification and confidence

---

## 🐛 Troubleshooting

### Backend won't start:
```bash
# Check Python version
python --version  # Should be 3.9+

# Check all files exist
ls backend/main.py
ls data/intents.json
ls data/faq.json

# Try verbose logging
python -m uvicorn backend.main:app --reload --log-level debug
```

### Dependencies won't install:
```bash
# Clear pip cache
pip cache purge

# Try installing with no cache
pip install --no-cache-dir -r requirements.txt
```

### spaCy model won't download:
```bash
# Manual download
python -c "import spacy; spacy.cli.download('en_core_web_sm')"
```

### Frontend won't connect to backend:
- ✅ Backend must be running on `http://localhost:8000`
- ✅ Check browser console for CORS errors (F12 → Console)
- ✅ Verify `frontend/chat.js` has correct API_BASE_URL

### Port conflicts:
```bash
# Find what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Use different port
python -m uvicorn backend.main:app --port 8001
# Update chat.js: const API_BASE_URL = 'http://localhost:8001'
```

---

## 📁 Project Structure After Setup

```
smart-customer-support-chatbot/
├── backend/
│   ├── __init__.py
│   ├── main.py              ← FastAPI app
│   ├── config.py            ← Settings
│   ├── database.py          ← DB models
│   ├── models.py            ← NLP models
│   ├── pipeline.py          ← Processing pipeline
│   ├── agent.py             ← AI agent logic
│   ├── schemas.py           ← Data schemas
│   ├── websocket_handler.py ← WebSocket
│   └── utils.py             ← Utilities
├── frontend/
│   ├── index.html           ← Chat UI
│   ├── style.css            ← Styling
│   └── chat.js              ← Client logic
├── data/
│   ├── intents.json         ← Intent definitions
│   └── faq.json             ← FAQ knowledge base
├── venv/                    ← Virtual environment
├── .env                     ← Configuration
├── .env.example             ← Template
├── requirements.txt         ← Dependencies
├── README.md                ← Documentation
└── chatbot.db               ← SQLite DB (created on first run)
```

---

## 🚀 Quick Summary

```bash
# 1. Activate venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 3. Create config
cp .env.example .env

# 4. Start backend (Terminal 1)
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 5. Test health (Terminal 2)
curl http://localhost:8000/health

# 6. Start HTTP server (Terminal 3)
python -m http.server 8080

# 7. Open browser
http://localhost:8080/frontend/index.html
```

---

## ✅ Next Steps After Setup

Once everything is running:

1. **Test different messages** in the chat UI
2. **Check browser console** (F12) for any JavaScript errors
3. **Check backend logs** in terminal for processing details
4. **Try API directly** with curl for different intents
5. **Create custom intents** by editing `data/intents.json`
6. **Add more FAQs** by editing `data/faq.json`

---

**Questions or errors? Provide the exact terminal output and I'll help fix it!**
