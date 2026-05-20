"""
Path setup for scene imports.
Import this at the top of each scene file before importing from utils.
"""
import sys
from pathlib import Path

# Add the project root (parent of scenes/) to sys.path
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
