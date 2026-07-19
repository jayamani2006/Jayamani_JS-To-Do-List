# Building from Source

## Prerequisites
- Python 3.8+
- Windows OS (for PyInstaller executable generation)

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jayamani2006/JS-To-Do-List.git
   cd JS-To-Do-List
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run from source:**
   ```bash
   python src/todo_app.py
   ```
   *Note: When running from source, the `data/` and `task_attachments/` folders will be created in your current working directory.*

## Building the Executable

To compile the standalone Windows executable, use the provided batch script or PyInstaller directly:

```bash
cd packaging
build_app.bat
```

This will run PyInstaller against `todo_app.spec` and copy the final `JS-To-Do-List.exe` to your Desktop.
