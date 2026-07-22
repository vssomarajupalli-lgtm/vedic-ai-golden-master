import os
import sys
from pathlib import Path

def get_app_data_dir() -> Path:
    """
    Returns the appropriate directory for persistent application data.
    - When running as a PyInstaller executable (frozen), routes to %APPDATA%/Samartha Vedic AI/database
    - When running in Dev/Docker, routes to the local repository database directory.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller bundled executable
        appdata = os.environ.get('APPDATA') or os.path.expanduser('~')
        data_dir = Path(appdata) / "Samartha Vedic AI" / "database"
    else:
        # Running in Development or Docker
        # Resolve path relative to this file: backend/app/core/paths.py -> backend/app/database
        data_dir = Path(__file__).resolve().parent.parent / "database"
    
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
