# src/config/project_paths.py

from pathlib import Path

def get_project_root() -> Path:
    """
    Traverse upward from this file to find the project root
    based on a known folder structure (e.g., presence of 'config' and 'src').
    """
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "src").exists() and (parent / "config").exists():
            return parent
    raise RuntimeError("Project root could not be determined.")
