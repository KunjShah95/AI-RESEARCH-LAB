@echo off
set PYTHONPATH=.
set DATABASE_URL=postgresql://postgres:HACKER_K@localhost:5432/paper_analyzer
set CRYPTO_SECRET_KEY=HACKER_K
set ENCRYPTION_KEY=HACKER_K

echo Starting Backend on http://localhost:8000...
cd /d C:\AI RESEARCH LAB\ai-research-lab
start "Backend" cmd /k "uvicorn --app-dir C:\AI RESEARCH LAB\ai-research-lab app.main:app --reload --host 0.0.0.0 --port 8001"

echo Starting Frontend on http://localhost:5173...
cd /d C:\AI RESEARCH LAB\ai-research-lab\frontend
start "Frontend" cmd /k "npm run dev"

echo.
echo Both servers should be starting now!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
pause