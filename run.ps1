$env:PYTHONPATH = "."
$env:DATABASE_URL = "postgresql://postgres:HACKER_K@localhost:5432/paper_analyzer"
$env:CRYPTO_SECRET_KEY = "HACKER_K"
$env:ENCRYPTION_KEY = "HACKER_K"

# Start backend in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\AI RESEARCH LAB\ai-research-lab'; uvicorn --app-dir . app.main:app --reload --host 0.0.0.0 --port 8001" -WindowStyle Normal

# Wait a bit
Start-Sleep -Seconds 2

# Start frontend
cd "C:\AI RESEARCH LAB\ai-research-lab\frontend"
npm run dev