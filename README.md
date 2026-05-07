# 🎓 AI Resume Builder — Enterprise-Grade Architecture

## 📁 Directory Structure

```
ai-resume-builder/
├── backend/
│   ├── services/
│   │   ├── __init__.py          # Makes services/ a Python package
│   │   └── groq_service.py      # Groq API wrapper (imports prompts, never defines them)
│   ├── .env                     # Environment variables (gitignored in production)
│   ├── app.py                   # Flask app: routes, error handlers, CORS
│   ├── config.py                # Centralised config loaded from .env
│   ├── prompts.py               # ★ ALL AI prompts live here and ONLY here
│   └── requirements.txt         # Python dependencies
│
└── frontend/
    ├── assets/
    │   ├── script.js            # API calls, state management, PDF/TXT export
    │   └── style.css            # Custom styles (glass-morphism, animations)
    └── index.html               # Main UI (Tailwind CDN, Marked.js, jsPDF)
```

---

## ⚙️ Architecture Notes (for your professor)

| Concern           | Location               | Rationale |
|-------------------|------------------------|-----------|
| **Prompts**       | `backend/prompts.py`   | Single source of truth for all LLM instructions. Independently versioned, testable, and swappable without touching service logic. |
| **Config**        | `backend/config.py`    | All `os.getenv()` calls centralised. No raw env reads anywhere else. |
| **AI Service**    | `backend/services/groq_service.py` | Pure service layer. Handles API communication and error translation. Imports prompts from `prompts.py`. |
| **Routing**       | `backend/app.py`       | Flask routes handle HTTP concerns only. Delegates AI work to the service layer. |
| **Frontend**      | `frontend/`            | Completely separated. Could be deployed to any CDN independently. |

---

## 🚀 Run Instructions

### 1. Clone / set up the project
```bash
# Navigate to the backend folder
cd ai-resume-builder/backend
```

### 2. Create and activate a virtual environment
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your API key
Open `backend/.env` and replace the placeholder:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```
Get a free key at → https://console.groq.com

### 5. Run the Flask backend
```bash
python app.py
```
You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### 6. Open the frontend
Open a **new terminal** and run:
```bash
# macOS
open ../frontend/index.html

# Linux
xdg-open ../frontend/index.html

# Windows
start ../frontend/index.html
```
Or simply drag `frontend/index.html` into your browser.

---

## 🔌 API Endpoints

| Method | Endpoint            | Description                        |
|--------|---------------------|------------------------------------|
| GET    | `/api/health`       | Liveness check + model info        |
| GET    | `/api/prompt-types` | Lists available document types     |
| POST   | `/api/generate`     | Main generation endpoint           |

### POST `/api/generate` — Request body
```json
{
  "prompt_type":        "resume",
  "job_title":          "Senior Full-Stack Engineer",
  "experience_level":   "Senior (6-10 years)",
  "key_skills":         "Python, React, PostgreSQL, Docker, AWS",
  "additional_context": "Targeting a Series B fintech startup"
}
```

### Response
```json
{
  "success":     true,
  "document":    "## Professional Summary\n...",
  "prompt_type": "resume",
  "job_title":   "Senior Full-Stack Engineer"
}
```

---

## ✨ Features
- **3 document types:** Resume, Cover Letter, LinkedIn Summary
- **ATS-optimised** output via expert-crafted system prompts
- **Real-time loading** skeleton animation while generating
- **Copy to Clipboard** (with toast confirmation)
- **Download as TXT** (plain text)
- **Download as PDF** (formatted with jsPDF — multi-page support)
- **Client-side validation** with inline error messages
- **API health badge** (auto-detects if backend is live)
- **Word count + section stats** displayed after generation
