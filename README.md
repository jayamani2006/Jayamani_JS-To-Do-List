<p align="center">
  <img src="assets/banner/hero-banner.png" alt="JS To-Do-List Hero Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/github/v/release/jayamani2006/JS-To-Do-List" alt="Latest Release">
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
</p>

## Overview

JS To-Do-List is a futuristic, fully offline task manager featuring rich file attachments and a decoupled state-machine architecture. Designed with a neon-glowing UI and 100% local SQLite storage, it solves the challenge of securely linking real-world files directly to your tasks without relying on external cloud providers.

## Key Features

- 📁 **Unlimited Folders:** Categorize your tasks efficiently.
- 📎 **Rich Attachments:** Add PDFs, DOCX, XLSX, MP3s, and Images directly to tasks.
- ⏱️ **Time Reference View:** Color-coded task urgency and feedback system.
- 🔄 **Midnight Watcher:** Automatically monitors and rolls over tasks at midnight.
- 🚀 **Portable Executable:** Single-file `.exe` requires no Python installation.

[View full feature list in docs/FEATURES.md](docs/FEATURES.md)

## Screenshots

<p align="center">
  <img src="assets/screenshots/main-window.png" alt="Main Window" width="45%">
  <img src="assets/screenshots/Task-Folder.png" alt="Folder Dashboard" width="45%">
</p>
<p align="center">
  <img src="assets/screenshots/Tasks-list.png" alt="Task Dashboard" width="45%">
  <img src="assets/screenshots/Task-page1.png" alt="Task Details" width="45%">
</p>

## Demo

<p align="center">
  <img src="assets/demo/demo.gif" alt="JS To-Do-List Demo GIF" width="80%">
</p>

> 🎥 **[Watch full video walkthrough (demo.mp4)](assets/demo/demo.mp4)**

## Installation

**For Users:**
Download the standalone portable `.exe` from [Releases](https://github.com/jayamani2006/JS-To-Do-List/releases). No Python needed. See [INSTALL.md](docs/INSTALL.md) for details.

**For Developers:**
See [BUILD.md](docs/BUILD.md) to set up a development environment and build from source.

## Requirements

- Windows 10/11
- Minimum 50 MB disk space

## Usage

1. Open the app.
2. Click "Add Task" to create a task in a folder.
3. Attach files or links if needed.
4. Mark complete and provide feedback.

[Read the full User Guide](docs/USER_GUIDE.md)

## Project Structure

```
JS-To-Do-List/
├── .github/          # GitHub templates & workflows
├── assets/           # UI media, banners, screenshots
├── docs/             # Technical documentation
├── packaging/        # PyInstaller specs & build scripts
├── sample_data/      # Demo database
└── src/              # Python application source
```

## Architecture

Built using Python, Tkinter, and an auto-migrating SQLite database, the app implements a robust state-machine pattern to decouple logic from the UI.
[Learn more in docs/PROJECT_ARCHITECTURE.md](docs/PROJECT_ARCHITECTURE.md)

## Performance

The app maintains sub-millisecond response times despite handling thousands of tasks, by utilizing SQLite efficiently and referencing local attachments without database bloat.

## Roadmap

- Variable difficulty modes
- Cross-platform support
- Enhanced keyboard shortcuts
[View full Roadmap](ROADMAP.md)

## FAQ

**Q: Where are attachments stored?**
A: Inside the `task_attachments/` folder locally.
[View full FAQ](docs/FAQ.md)

## License

[MIT License](LICENSE)

## Developer

Built by **Jayasubramani** (Chip-X, JS SoftTools)

## Support

Report a bug: [Open Issue](https://github.com/jayamani2006/JS-To-Do-List/issues/new?template=bug_report.md)
Request a feature: [Suggest Feature](https://github.com/jayamani2006/JS-To-Do-List/issues/new?template=feature_request.md)

## Download

[Download Latest Release](https://github.com/jayamani2006/JS-To-Do-List/releases/latest)

---
*Acknowledgements: Uses `tkcalendar` and `Pillow`. Built with PyInstaller.*
