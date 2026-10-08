# CSE3CAP - EPlacementBrief

## About
Team DD's EPlacement Brief project for CSE3CAP.

The Django starter project is set up. Placement features are currently being developed.

## Setup on Windows
Install Python 3.14 and clone this repository. Open the project folder in VS Code, then run these commands one at a time in the terminal:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

Press Ctrl+C in the terminal to stop the server.