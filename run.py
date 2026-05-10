#!/usr/bin/env python
import os
import sys

# Get the directory where run.py is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Add current directory to Python path
sys.path.insert(0, script_dir)

# Import and run uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        env_file=".env",
        app_dir=script_dir,
    )
