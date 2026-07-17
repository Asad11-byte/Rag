import os
import sys
from pathlib import Path

# 1. Resolve Python paths so 'backend' is recognized
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
backend_dir = project_root / "backend"

# Insert 'backend' into Python's search path so 'import app' works perfectly
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# 2. Safely import your FastAPI app instance from app/main.py
from app.main import app

# 3. Dynamic route prefix mapping
# When running on Vercel, this automatically strips the "/api" prefix from incoming requests.
# This makes your '/api/documents' request map perfectly to '@router.get("/documents")'!
if os.environ.get("VERCEL"):
    app.root_path = "/api"