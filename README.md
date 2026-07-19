<p align="center">
  <img src="assets/icons/JSSTP logo.jpg" alt="JS SoftTools Logo" width="120" style="border-radius: 50%;">
</p>

> **IMPORTANT:** This software is developed for student learning and educational purposes only.

<p align="center">
  <img src="assets/banner/hero-banner.png" alt="JS To-Do-List Banner" width="100%">
</p>

<h1 align="center">JS To-Do-List</h1>

<p align="center">
  <strong>Team: Chip-X | Developer: Jayasubramani S</strong>
</p>

<p align="center">
  <strong>A futuristic, offline task manager featuring rich file attachments and smart task organization.</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/jayamani2006/Jayamani_JS-To-Do-List.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/platform-windows-blue.svg" alt="Platform">
  <img src="https://img.shields.io/badge/made_with-Python_|_Tkinter-yellow.svg" alt="Made with Python/Tkinter">
  <a href="https://github.com/jayamani2006/Jayamani_JS-To-Do-List/releases/latest"><img src="https://img.shields.io/github/v/release/jayamani2006/Jayamani_JS-To-Do-List.svg" alt="Latest Release"></a>
  <img src="https://img.shields.io/github/repo-size/jayamani2006/Jayamani_JS-To-Do-List.svg" alt="Repo Size">
</p>

---

JS To-Do-List is a futuristic, fully offline task manager developed by **Jayasubramani** under the **Chip-X / JS SoftTools** brand. Built as a portfolio project, it features rich file attachments, a unique Time Reference view, a Midnight Watcher for daily tasks, and a standalone Windows executable — all stored 100% locally with no cloud dependency.

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Demo](#demo)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Building from Source](#building-from-source)
- [Roadmap](#roadmap)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)
- [Developer](#developer)
- [Support](#support)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Unlimited Folders** — Categorize your tasks into as many folders as you need.
- **Rich Attachments** — Attach PDFs, DOCX, XLSX, MP3s, and Images directly to any task.
- **Time Reference View** — Color-coded urgency system: Green (on track), Yellow (approaching), Red (overdue).
- **Midnight Watcher** — Automatically monitors and rolls over daily/repeating tasks at midnight.
- **Task Feedback System** — Rate completed tasks with emoji-based feedback ratings.
- **Portable Executable** — Single-file `.exe`, no Python installation required for end users.

*See [docs/FEATURES.md](docs/FEATURES.md) for the full feature list.*

---

## Screenshots

<table align="center">
  <tr>
    <td><img src="assets/screenshots/main-window.png" alt="Main Dashboard" width="400"></td>
    <td><img src="assets/screenshots/Tasks-list.png" alt="Task List View" width="400"></td>
  </tr>
  <tr>
    <td align="center"><strong>Main Dashboard</strong></td>
    <td align="center"><strong>Task List View</strong></td>
  </tr>
  <tr>
    <td><img src="assets/screenshots/Task-page1.png" alt="Task Details - Part 1" width="400"></td>
    <td><img src="assets/screenshots/Task-page2.png" alt="Task Details - Part 2" width="400"></td>
  </tr>
  <tr>
    <td align="center"><strong>Task Details (Top)</strong></td>
    <td align="center"><strong>Task Details (Bottom)</strong></td>
  </tr>
  <tr>
    <td colspan="2" align="center"><img src="assets/screenshots/Task-Folder.png" alt="Folder Dashboard" width="400"></td>
  </tr>
  <tr>
    <td colspan="2" align="center"><strong>Folder Dashboard</strong></td>
  </tr>
</table>

---

## Demo

<p align="center">
  <img src="assets/demo/demo.gif" alt="JS To-Do-List Demo GIF" width="100%">
</p>

> 🎥 **[Watch full MP4 walkthrough (demo.mp4)](assets/demo/demo.mp4)**

---

## Installation

**Portable EXE (Recommended)**
1. Download `JS-To-Do-List-v1.0.0-windows-x64.exe` from [Releases](https://github.com/jayamani2006/Jayamani_JS-To-Do-List/releases/latest).
2. Double-click to run instantly. No installation required.

*See [docs/INSTALL.md](docs/INSTALL.md) for detailed instructions.*

---

## Requirements

- **OS:** Windows 10 or 11 (64-bit)
- **Dependencies:** None required for the portable executable.
- **Storage:** Minimum 50 MB disk space.

---

<p align="center">
  <img src="assets/icons/JSSTP logo.jpg" alt="JS SoftTools Logo" width="60" style="border-radius: 50%;">
  &nbsp;&nbsp;
  <img src="assets/icons/icon.ico" alt="JS To-Do-List App Icon" width="60">
</p>

<p align="center">
  <em>Built by JS SoftTools · Chip-X Team</em>
</p>

---

## Usage

1. **Open the app.**
2. **Create Folders** — Use the left sidebar to add and organize folders.
3. **Add Tasks** — Click "Add Task" inside any folder.
4. **Attach Files** — Link any local file (PDF, image, audio, document) directly to a task.
5. **Track Progress** — Use the Time Reference view to see color-coded urgency.
6. **Complete & Rate** — Mark tasks complete and leave an emoji feedback rating.

*See [docs/USER_GUIDE.md](docs/USER_GUIDE.md) for full application instructions.*

---

## Project Structure

<details>
<summary>Click to expand folder tree</summary>

```
JS-To-Do-List/
├── .github/          # GitHub Actions CI workflows & issue templates
├── assets/           # UI media — banners, screenshots, demo videos, icons
│   ├── banner/       # Hero banners
│   ├── demo/         # GIF and MP4 demo files
│   ├── icons/        # App icon and brand logo
│   └── screenshots/  # Application UI screenshots
├── docs/             # Technical documentation
├── packaging/        # PyInstaller specs & build scripts
├── sample_data/      # Demo seed database
├── src/              # Python application source
│   ├── todo_app.py   # Main application (Tkinter + SQLite)
│   └── welcome.py    # Neon launcher splash screen
└── [Config Files]    # README, LICENSE, CHANGELOG, requirements.txt, etc.
```

</details>

---

## Architecture

Built using Python, Tkinter, and an auto-migrating SQLite database (`js_todo.db`), the app uses a clean state-machine pattern to decouple UI logic from data operations.

- The SQLite database is dynamically generated on first launch — no setup required.
- Local file attachments are referenced by path, keeping the database lightweight.
- A background thread monitors midnight to auto-reset daily repeating tasks.

*Read the full technical breakdown in [docs/PROJECT_ARCHITECTURE.md](docs/PROJECT_ARCHITECTURE.md).*

---

## Building from Source

1. Clone the repo and create a virtual environment (`Python 3.8+`).
2. Install dependencies: `pip install -r requirements.txt`
3. Run directly: `python src/todo_app.py`
4. Build EXE: run `packaging/build_app.bat`

*See [docs/BUILD.md](docs/BUILD.md) for detailed build instructions.*

---

## Roadmap

- Cross-platform support (Linux, macOS)
- Cloud sync option (optional, local-first by default)
- Enhanced keyboard shortcuts and accessibility

*See [ROADMAP.md](ROADMAP.md) for the full list of planned improvements.*

---

## FAQ

**Q: Where are my attachments stored?**
A: Inside the `task_attachments/` folder on your local machine, next to the database.

**Q: Is my data private?**
A: Yes. Everything is 100% local. No internet connection is required or used.

*Read more in [docs/FAQ.md](docs/FAQ.md).*

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community guidelines.

---

## License

This project is licensed under the [MIT License](LICENSE).
Please also read [DISCLAIMER.md](DISCLAIMER.md) regarding usage and limitations.

---

## Developer

<p align="center">
  <img src="assets/icons/JSSTP logo.jpg" alt="JS SoftTools" width="80" style="border-radius: 50%;">
</p>

<p align="center">
  Developed by <strong>Jayasubramani</strong><br>
  Founder · JS SoftTools · Chip-X Team<br>
  B.E. Electrical & Electronics Engineering · Knowledge Institute of Technology · Anna University · Class of 2027
</p>

---

## Support

Found a bug or have a feature request?

- 🐛 [Report a Bug](https://github.com/jayamani2006/Jayamani_JS-To-Do-List/issues/new?template=bug_report.md)
- 💡 [Request a Feature](https://github.com/jayamani2006/Jayamani_JS-To-Do-List/issues/new?template=feature_request.md)

---

## Acknowledgements

- Built with Python's standard `tkinter` and `sqlite3` libraries
- Calendar picker powered by [`tkcalendar`](https://tkcalendar.readthedocs.io/)
- Image handling via [`Pillow`](https://pillow.readthedocs.io/)
- Packaged with [PyInstaller](https://pyinstaller.org/)

---

> **IMPORTANT:** This software is developed for student learning and educational purposes only. It is a portfolio project and not intended for commercial production use.
