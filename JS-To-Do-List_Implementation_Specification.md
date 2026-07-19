# JS To-Do-List — World-Class Repository Implementation Specification

**Document type:** Engineering / Repository Transformation Specification
**Prepared for:** Jayasubramani (JS SoftTools / Chip-X)
**Subject application:** JS To-Do-List (Python / Tkinter desktop task manager)
**Purpose:** A complete, unambiguous instruction set that another coding AI (or Jayasubramani) can execute end-to-end to turn the current working folder into a professionally maintained, portfolio-grade, recruiter-ready GitHub repository — **without changing app functionality.**

This document does not contain code, does not contain a README draft, and does not contain a LinkedIn post. It is the blueprint that produces all of those artifacts in a later execution pass.

---

## PHASE 0 — Inspection Summary (What Was Actually Found)

The uploaded archive (`1784108011670_To-Do-List.rar`) was extracted and every file inspected. Actual contents:

| Path | Size | What it is |
|---|---|---|
| `todo_app.py` | 1,208 lines / ~49 KB | Main application — single-file Tkinter + SQLite to-do app. Classes: `TaskModal`, `TodoApp`. ~20 top-level DB helper functions. |
| `welcome.py` | 128 lines | A separate Tkinter "splash/welcome" launcher window with a neon-glow UI. |
| `todo_app.spec` | 24 lines | PyInstaller spec — builds `todo_app.py` into `todo_app.exe`, bundles `icon.ico`. Portable (no hardcoded paths). |
| `welcome.spec` | 27 lines | PyInstaller spec for `welcome.py`. **Contains hardcoded absolute paths**: `E:\Chip-X\JS To-Do-List\To-Do-List\welcome.py` and `E:\DEVELPOMENT files\To-Do-List\icon.ico`. |
| `main.spec` | 23 lines | PyInstaller spec referencing a **`main.py` that does not exist anywhere in the archive.** Orphaned/dead build artifact. |
| `build_app.bat` + duplicate `build_app.bat.txt` | 8 lines each | Batch script: builds EXE with PyInstaller, copies to Desktop, shows a VBScript popup. Only ever builds `todo_app.py`, never `welcome.py` or `main.py`. |
| `notify.vbs` + duplicate `notify.vbs.txt` | 1 line each | A single `MsgBox` popup ("Build Complete"). Trivial, duplicated for no reason. |
| `icon.ico` | 894 KB | Application icon — unusually large for a `.ico` (likely contains oversized frames or an embedded PNG at very high resolution). |
| `js_todo.db` | 28 KB | **Live SQLite database containing the developer's real personal task data** (task names like "want to refer book", real due dates from Oct 2025, personal notes). This must never ship in a public repository. |
| `dist/js_todo.db` | 0 bytes | Empty/corrupt duplicate DB left over from a build run. |
| `dist/todo_app.exe` | 38.4 MB | Compiled Windows executable — a build output, should never be committed to source control. |
| `build/main/`, `build/todo_app/`, `build/welcome/` | 139 MB combined | Full PyInstaller intermediate build caches (`.pyc`, `.toc`, `xref-*.html`, `warn-*.txt`, `localpycs/`). 100% disposable, regenerable, and currently the single largest contributor to repository bloat. |
| `outputs/workspace_output_1760363966_7605.txt`, `..._3663.txt` (0 bytes), `..._JS_TODO_APP_PROJECT_1098.txt` (80 KB) | ~85 KB | Raw terminal/pip-install logs and what appears to be an AI-assistant session transcript/log from development. Not project documentation — internal scratch output. |
| `data/` | empty | Empty folder, currently serves no purpose (git does not track empty folders anyway). |
| `task_attachments/f1_t7/`, `task_attachments/f21_t3/`, `task_attachments/f1_t4/`, `task_attachments/f7_t1/` | ~14 MB | **Real personal file attachments** — a personal ChatGPT-generated image and an MP3 song ("in the stars") attached to real tasks. Personal media, not sample/demo data, and duplicated (same PNG appears twice under two different task folders). |
| `task_attachments/tasks.txt` | 0 bytes | Empty stray file with no evident purpose in the code (the code never reads/writes a file named exactly `tasks.txt` at that path — it's a leftover). |
| `README.md` | 66 lines | Existing README — reasonable tone but structurally incomplete: several sections ("Opening the App", "Installation" steps 2 and 4) reference actions with no actual command/path text filled in; "Folder Structure" section header exists with no content beneath it. |

### What is good
- The application logic itself is functionally complete: full CRUD for tasks/folders, attachments, links, daily-repeat automation, a midnight watcher, dark theme, and a DB auto-migration routine (`init_db()` adds missing columns safely) — this is a genuinely thoughtful touch that shows engineering maturity.
- Consistent branding (JS SoftTools / Chip-X, dark navy/cyan neon aesthetic) across `welcome.py` and the README.
- `todo_app.spec` is portable and correctly bundles the icon.
- The existing README has the right instinct (Features → Installation → Folder Structure) even though it's incomplete.

### What is acceptable
- Single-file `todo_app.py` architecture is acceptable for a project of this size, though it will be flagged in Phase 2 as a target for light modularization (optional, not required, since "do not change functionality" takes priority).
- `icon.ico` is usable as-is, just oversized for what it needs to be.

### What looks unprofessional
- Two duplicate "junk twin" files exist for no functional reason: `build_app.bat.txt` (identical to `build_app.bat`) and `notify.vbs.txt` (identical to `notify.vbs`). These look like accidental drag-and-drop duplicates and must be removed.
- `main.spec` references a `main.py` that doesn't exist — a dead, confusing artifact for anyone reading the repo.
- Hardcoded developer machine paths (`E:\Chip-X\...`, `E:\DEVELPOMENT files\...`) inside `welcome.spec` and inside `welcome.py`'s `open_app()` and logo-loading logic. This leaks the developer's local folder structure and breaks the moment anyone else tries to build it.
- The `outputs/` folder is a raw AI/pip session log directory — it reads as "someone forgot to delete their terminal scrollback," not as project documentation.

### What should be removed (before first commit)
- `build/` (139 MB of PyInstaller cache — regenerable, never belongs in git)
- `dist/` (38 MB compiled `.exe` + empty duplicate `.db` — build output, never belongs in git)
- `outputs/` (raw logs/transcripts — internal scratch, not documentation)
- `build_app.bat.txt`, `notify.vbs.txt` (exact duplicates of real files)
- `main.spec` (references nonexistent `main.py`)
- `data/` (empty, purposeless folder)
- `task_attachments/tasks.txt` (empty, unreferenced by code)
- `js_todo.db` and `dist/js_todo.db` (real personal data — replace with a fresh, empty schema-only DB or generate one at first run, never ship personal data)
- Real personal files under `task_attachments/f1_t7/`, `task_attachments/f21_t3/`, `task_attachments/f1_t4/`, `task_attachments/f7_t1/` — personal photo and MP3, not sample data

### Dead / duplicate files (explicit list)
| File | Status |
|---|---|
| `build_app.bat.txt` | Exact duplicate of `build_app.bat` |
| `notify.vbs.txt` | Exact duplicate of `notify.vbs` |
| `main.spec` | Dead — references missing `main.py` |
| `dist/js_todo.db` | Empty/corrupt duplicate of root `js_todo.db` |
| `task_attachments/f1_t7/ChatGPT Image Oct 13, 2025, 01_39_00 PM.png` and the identical copy under `f21_t3/` | Duplicate binary (same file, two folders) |

### Security / privacy risks (explicit list)
1. **Personal task data in `js_todo.db`** — real task titles, dates, and notes belonging to the developer. Must be scrubbed before any public push.
2. **Personal media in `task_attachments/`** — a real photo and a real MP3 tied to real tasks. Must be scrubbed.
3. **Hardcoded local absolute paths** in `welcome.spec` and `welcome.py` reveal folder-naming conventions of the developer's machine (`E:\Chip-X\...`, `E:\DEVELPOMENT files\...`). Low severity but unprofessional and breaks portability.
4. **`outputs/*.txt`** may contain incidental personal/system info from a dev machine (usernames, paths, pip cache paths) — must not be published verbatim.
5. No `.gitignore` currently exists, so none of the above are currently prevented from being committed by tooling — this is a process risk, not just a content risk.

### Missing files (repo hygiene)
No `.gitignore`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `.github/` folder, GitHub Actions, issue/PR templates, `requirements.txt`, `CONTRIBUTING` guidance, or versioning file of any kind currently exist. Full list and specs are in Phase 4.

### Bad naming
- `todo_app.exe` (build output name) vs. `JS To-Do-List.exe` (name used in `welcome.py`'s launch path and in `build_app.bat`'s copy step) — two different names refer to the same artifact across the codebase. This must be standardized (Phase 3).
- Folder `task_attachments` subfolders use an internal code (`f1_t7`, `f21_t3`) which is fine as an internal storage scheme but should never be exposed as "sample data" in a repo without renaming to something self-explanatory if kept as demo content.

### Poor architecture / structure observations
- Everything (app code, build scripts, build cache, build output, personal database, personal attachments, dev logs) currently lives flat in one folder with no separation between **source**, **build artifacts**, **user data**, and **documentation**. This is the single biggest structural issue and is fully addressed in Phase 2.
- There is no dependency manifest (`requirements.txt`) despite the code depending on `tkcalendar` and `Pillow` (confirmed by import statements and by the pip log found in `outputs/`).

---

## PHASE 1 — Full Inspection Findings (Consolidated Checklist)

- [x] Every folder inspected (`build/`, `data/`, `dist/`, `outputs/`, `task_attachments/`, root)
- [x] Every file inspected (13 root files + nested build/attachment files)
- [x] Every asset inspected (`icon.ico`, PNG, MP3)
- [x] Every configuration inspected (3 `.spec` files, `build_app.bat`, `notify.vbs`)
- [x] Every dependency identified (`tkinter` [stdlib], `tkcalendar`, `Pillow`, `sqlite3` [stdlib], `webbrowser` [stdlib])
- [x] Every executable inspected (`dist/todo_app.exe`)
- [x] Installer inspected — **note:** there is no true installer (no Inno Setup script, no NSIS script); `build_app.bat` is a build-and-copy-to-desktop script, not an installer. This should be labeled accurately everywhere (README currently implies "Installer will…", which is inaccurate — it's a build script).
- [x] Icon inspected (oversized `.ico`, flagged for optimization)
- [x] Images inspected (personal ChatGPT-generated PNG, flagged as private data)
- [x] Documentation inspected (`README.md` — incomplete)
- [x] Dead files identified (see table above)
- [x] Duplicate files identified (see table above)
- [x] Unused assets identified (`data/`, `task_attachments/tasks.txt`)
- [x] Temporary/cache files identified (entire `build/` tree)
- [x] Missing files identified (Phase 4)
- [x] Security risks identified (personal DB, personal media, hardcoded paths)
- [x] Naming inconsistencies identified (`todo_app.exe` vs `JS To-Do-List.exe`)

---

## PHASE 2 — Ideal Repository Structure

```
JS-To-Do-List/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── build-windows.yml
│       └── release.yml
├── assets/
│   ├── icons/
│   │   └── icon.ico
│   ├── screenshots/
│   │   ├── main-window.png
│   │   ├── add-task-modal.png
│   │   ├── task-detail-view.png
│   │   ├── time-reference-view.png
│   │   ├── completed-tasks-tab.png
│   │   └── welcome-screen.png
│   ├── banner/
│   │   ├── hero-banner.png
│   │   └── social-preview.png
│   └── demo/
│       ├── demo.gif
│       └── demo.mp4
├── docs/
│   ├── INSTALL.md
│   ├── USER_GUIDE.md
│   ├── BUILD.md
│   ├── PROJECT_ARCHITECTURE.md
│   ├── FEATURES.md
│   ├── FAQ.md
│   └── KNOWN_ISSUES.md
├── src/
│   ├── todo_app.py
│   └── welcome.py
├── packaging/
│   ├── todo_app.spec
│   ├── welcome.spec
│   └── build_app.bat
├── sample_data/
│   └── (optional) demo_seed.db — a fresh DB with 3-4 fictional example tasks, no personal data
├── .gitignore
├── LICENSE
├── README.md
├── CHANGELOG.md
├── ROADMAP.md
├── SECURITY.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── DISCLAIMER.md
├── VERSION
└── requirements.txt
```

### Folder-by-folder rationale

| Folder | Purpose | Contents | Why it belongs | Naming convention |
|---|---|---|---|---|
| `.github/` | GitHub-native automation & community health files | Issue templates, PR template, Actions workflows | GitHub auto-detects this folder for templates and CI; industry-standard location | lowercase, GitHub-reserved name |
| `assets/` | All non-code visual/media assets used in docs and the repo page | Icons, screenshots, banners, demo GIF/MP4 | Keeps binary media out of the source tree; makes README embeds trivial (`assets/screenshots/...`) | lowercase, plural, grouped by type |
| `docs/` | Long-form documentation that doesn't belong inline in the README | Install/build/architecture/FAQ docs | Keeps root clean; README becomes a landing page linking into `docs/` | UPPER_SNAKE for doc files (GitHub convention) |
| `src/` | Actual application source code only | `todo_app.py`, `welcome.py` | Standard convention signals "this is the real source," separate from packaging/build tooling | lowercase |
| `packaging/` | Everything needed to reproduce a Windows build | `.spec` files, `build_app.bat` | Separates "how we ship this" from "what the app is"; makes it obvious these are build-only files | lowercase |
| `sample_data/` (optional) | Non-personal demo content only, if the developer wants the repo to be runnable out-of-the-box | Empty/seed DB with fictional tasks | Lets a stranger clone-and-run without ever touching real personal data | lowercase |
| Root | Entry points and GitHub-standard community/legal files | `README.md`, `LICENSE`, etc. | GitHub explicitly looks for these exact filenames at repo root to render badges/links automatically | Exact GitHub-recognized filenames |

**Example hierarchy in practice:** a new visitor lands on `README.md` → sees badges, hero banner, and a feature GIF pulled from `assets/` → clicks "Full Installation Guide" which points to `docs/INSTALL.md` → clicks "Building from Source" which points to `docs/BUILD.md` and references `packaging/build_app.bat`.

---

## PHASE 3 — File Rename Plan

| Old Name | → | New Name | Reason |
|---|---|---|---|
| `todo_app.py` | → | `src/todo_app.py` (name unchanged, path changed) | Move into `src/` for structure; name itself is already clear and matches its `.spec` and `.exe`, so no rename needed |
| `welcome.py` | → | `src/welcome.py` | Same — path change only |
| `dist/todo_app.exe` (build output) | → | *(not renamed — this file should not be tracked in git at all; see Phase 6/11 for release naming: `JS-ToDo-List-vX.Y.Z-windows-x64.exe`)* | Build artifact naming belongs to the Release process, not the source tree |
| `build_app.bat.txt` | → | *(delete — duplicate)* | Exact duplicate of `build_app.bat`; no reason to keep both |
| `notify.vbs.txt` | → | *(delete — duplicate)* | Exact duplicate of `notify.vbs` |
| `main.spec` | → | *(delete — dead file)* | References a `main.py` that does not exist anywhere in the project |
| `todo_app.spec` | → | `packaging/todo_app.spec` | Path change only; move into `packaging/` |
| `welcome.spec` | → | `packaging/welcome.spec` — **and edit hardcoded paths to relative paths** (`welcome.py`, `../assets/icons/icon.ico`) | Removes developer's personal machine path; makes the build reproducible on any machine |
| `build_app.bat` | → | `packaging/build_app.bat` — **and update internal comment to clarify it produces `JS-To-Do-List.exe` naming consistently** | Path change + naming consistency fix (see below) |
| `icon.ico` | → | `assets/icons/icon.ico` | Grouped with other visual assets |
| `js_todo.db` (real personal data) | → | *(delete from repo; optionally replace with `sample_data/demo_seed.db` containing fictional tasks only)* | Personal data must never be committed |
| `dist/js_todo.db` (empty duplicate) | → | *(delete)* | Corrupt/empty leftover build artifact |
| `data/` (empty folder) | → | *(delete)* | Serves no purpose; the app already creates this folder at runtime via `os.makedirs` |
| `task_attachments/` (entire folder, real personal media) | → | *(delete from repo entirely)* | Contains real personal photo + MP3; the app already creates this folder and its subfolders at runtime, so nothing needs to ship |
| `task_attachments/tasks.txt` | → | *(delete)* | Empty, unreferenced by any code path |
| `outputs/` (entire folder) | → | *(delete)* | Raw AI/pip session logs, not documentation |
| `build/` (entire folder, 139 MB) | → | *(delete)* | PyInstaller cache, 100% regenerable |
| `dist/` (entire folder) | → | *(delete from git — keep locally only, or publish only via GitHub Releases, never via source control)* | Compiled binaries do not belong in source history |

### Naming convention explanation
Professional repositories follow these conventions, which this plan applies:
- **Documentation files**: `UPPER_SNAKE_CASE.md` at root (e.g., `CONTRIBUTING.md`, `SECURITY.md`) — this is a GitHub-recognized convention that triggers special UI treatment (e.g., GitHub shows a banner linking to `SECURITY.md` on the repo's Security tab).
- **Source files**: `lower_snake_case.py`, matching existing convention in `todo_app.py`/`welcome.py` — no change needed, already correct.
- **Folders**: all-lowercase, plural when they contain collections of similar items (`docs/`, `screenshots/`, `icons/`).
- **Release binaries**: `ProjectName-vMAJOR.MINOR.PATCH-platform-arch.exe` (e.g., `JS-To-Do-List-v1.0.0-windows-x64.exe`) — self-describing filenames so a user who only has the downloaded file (no context) still knows exactly what it is, what version, and what platform.
- **One canonical product name everywhere.** Currently the app is called "JS To-Do-List" (README/welcome.py) but also "todo_app" (spec/exe filenames). Standardize on **"JS To-Do-List"** as the human-facing name and `todo_app` as the internal Python module/file name (this is normal — e.g., "Visual Studio Code" ships as `code.exe`). The one place that must be fixed is `build_app.bat`'s copy step, which should copy to `JS-To-Do-List.exe` on the Desktop consistently, matching what `welcome.py` expects to launch.

---

## PHASE 4 — Files That Must Be Created

| File | Purpose | Contents | Why it matters | Approx. length |
|---|---|---|---|---|
| `README.md` (rewrite) | Front door of the repo | See Phase 5 blueprint | First impression for every visitor | 250–400 lines |
| `LICENSE` | Legal terms of use/reuse | Full text of chosen license (MIT recommended for a portfolio project — permissive, well-understood, doesn't restrict personal/recruiter viewing) | GitHub will show a "License" badge and tab automatically; without it the code is technically "all rights reserved" by default, which looks unprofessional and confuses potential employers/collaborators | Standard license boilerplate (~20–200 lines depending on license) |
| `CHANGELOG.md` | Version history | Reverse-chronological list of versions with Added/Changed/Fixed/Removed sections (Keep a Changelog format) | Shows the project is actively maintained and versioned like real software | Grows over time; start with 1 entry (`v1.0.0`) |
| `ROADMAP.md` | Future direction | Checklist of planned features (e.g., cloud sync, mobile companion, cross-platform build) with rough priority/status | Signals ongoing intent and vision — attractive to recruiters and contributors | 40–80 lines |
| `SECURITY.md` | Vulnerability reporting policy | Supported versions table + how to privately report a security issue (email/contact) | Required by GitHub's community-profile checklist; signals security-consciousness | 20–40 lines |
| `CONTRIBUTING.md` | How outside developers can contribute | Branching model, code style, how to open a PR, how to run locally | Needed the moment anyone besides the author wants to submit a PR | 60–120 lines |
| `CODE_OF_CONDUCT.md` | Community behavior standard | Contributor Covenant (industry-standard template) | Completes GitHub's "Community Standards" checklist (visible under Insights → Community) | Standard template (~75 lines) |
| `docs/INSTALL.md` | Step-by-step install instructions for end users (non-developers) | Download link, unzip/run steps, screenshots of first launch | Separates "how do I use this app" from "how do I build it," which the current single README conflates | 60–100 lines |
| `docs/USER_GUIDE.md` | Full feature walkthrough | Every feature (folders, tasks, attachments, links, daily-repeat, feedback ratings, Time Reference view) explained with screenshots | Turns the app from "a script" into "a documented product" | 150–250 lines |
| `docs/BUILD.md` | How to build the EXE from source | Prerequisites, `pip install -r requirements.txt`, running `packaging/build_app.bat`, expected output location | Needed for any developer/contributor who wants to build locally | 40–80 lines |
| `docs/PROJECT_ARCHITECTURE.md` | Technical design explanation | DB schema diagram (folders/tasks/attachments/task_links tables + relationships), app class structure (`TodoApp`, `TaskModal`), data flow for attachments, the daily-repeat "midnight watcher" mechanism | Demonstrates engineering depth to technical reviewers | 100–200 lines |
| `docs/FEATURES.md` | Exhaustive feature list | Bullet list expanding what's currently condensed into the README's "Special Features" section | Gives recruiters/users a scannable feature inventory | 40–80 lines |
| `docs/FAQ.md` | Common questions | E.g., "Where are my attachments stored?", "Is my data sent anywhere? (No — fully offline/local SQLite)", "Can I use this on Mac/Linux?" | Reduces repeat issues/questions | 30–60 lines |
| `docs/KNOWN_ISSUES.md` | Transparency about current limitations | e.g., "Windows-only currently," "No cloud backup," "Large attachments increase folder size linearly" | Professional projects disclose limitations rather than hide them | 20–40 lines |
| `DISCLAIMER.md` | Liability/usage disclaimer | Standard "provided as-is, no warranty, use at your own risk" language, plus a note that it is an independent/personal project not affiliated with any employer | Protects the author, standard for solo/portfolio OSS projects | 15–25 lines |
| `VERSION` | Single source of truth for current version | Plain text, e.g. `1.0.0` | Some CI/release scripts read this file directly rather than parsing tags | 1 line |
| `.gitignore` | Prevent build/cache/personal-data files from ever being committed | Entries for `build/`, `dist/`, `__pycache__/`, `*.pyc`, `*.spec.bak`, `js_todo.db`, `task_attachments/`, `outputs/`, `data/`, `.vscode/`, `*.log` | This is the single most important file for preventing the exact privacy/bloat issues found in Phase 1 from recurring | 20–40 lines |
| `requirements.txt` | Pinned Python dependencies | `tkcalendar==1.6.1`, `pillow>=10.2.0`, `pyinstaller` (dev-only, can be in a separate `requirements-dev.txt`) | Currently completely absent; without it nobody can reliably set up a dev environment | 3–6 lines |
| `.github/ISSUE_TEMPLATE/bug_report.md` | Structured bug reports | Fields: description, steps to reproduce, expected/actual behavior, screenshots, OS/version | Raises quality of incoming issues | 20–30 lines |
| `.github/ISSUE_TEMPLATE/feature_request.md` | Structured feature suggestions | Fields: problem statement, proposed solution, alternatives considered | Same as above, for features | 15–25 lines |
| `.github/PULL_REQUEST_TEMPLATE.md` | Structured PR descriptions | Checklist: description, related issue, testing done, screenshots if UI change | Keeps PR quality consistent | 15–20 lines |
| `.github/workflows/build-windows.yml` | CI: verify the app still builds on every push | Sets up Python, installs `requirements.txt`, runs PyInstaller against `packaging/todo_app.spec`, uploads the EXE as a build artifact | Shows "this repo has automated verification," a strong trust signal | ~30–50 lines of YAML |
| `.github/workflows/release.yml` | CD: automatically attach the built EXE to a GitHub Release when a version tag is pushed | Triggers on `v*` tags, builds, zips, uploads to the Release | Professional release automation, referenced in Phase 11 | ~30–50 lines of YAML |

---

## PHASE 5 — README Master Blueprint (Structure Only, Not Final Copy)

Section order and exact content guidance for the rewritten `README.md`:

1. **Hero Banner** — full-width image (`assets/banner/hero-banner.png`), dark navy/cyan theme matching the app, containing the app name and a one-line tagline (e.g., "A futuristic, fully offline task manager with rich file attachments").
2. **Badges row** — directly under the banner: license badge, latest release badge, platform badge ("Windows"), Python version badge, build-status badge (once CI exists), "maintained" badge.
3. **One-paragraph introduction** — what the app is, who it's for, why it's different (offline, rich attachments, JS-branded UI). Pulled/expanded from the existing intro paragraph, which is already good.
4. **Feature highlights** — condensed bullet list (5–8 top features), with a link to the full `docs/FEATURES.md` for the exhaustive list.
5. **Screenshots gallery** — 3–5 embedded screenshots side by side or stacked, captioned (main window, add-task modal, Time Reference view).
6. **Animated GIF demo** — a single looping GIF (10–20s) showing add → attach → complete-with-feedback flow, embedded right after screenshots.
7. **Demo video link** — a linked thumbnail or badge pointing to a hosted `demo.mp4` (or YouTube link if the author later uploads one) for a fuller walkthrough than the GIF.
8. **Installation** — two clear sub-paths: "For Users" (download the `.exe` from Releases, no Python needed) linking to `docs/INSTALL.md`, and "For Developers" (clone + `pip install -r requirements.txt` + run `src/todo_app.py`) linking to `docs/BUILD.md`.
9. **Requirements** — OS (Windows 10/11), Python version if building from source, disk space note.
10. **Usage** — a short quick-start (Add Task → Attach File → Set Due Date → Mark Complete), linking to the full `docs/USER_GUIDE.md`.
11. **Controls / Shortcuts** — any keyboard shortcuts or UI conventions worth documenting (if none currently exist, state that navigation is fully mouse-driven, and list this as a `ROADMAP.md` item to add shortcuts later).
12. **Project Structure** — a fenced code block showing the Phase 2 folder tree, so visitors immediately understand the repo layout without opening every folder.
13. **Architecture** — 2–3 sentence summary plus a link to `docs/PROJECT_ARCHITECTURE.md` for the full DB-schema/class-diagram breakdown.
14. **Performance notes** — e.g., "SQLite storage keeps the app instant even with thousands of tasks; attachments are referenced by path, not duplicated in the database."
15. **Roadmap** — 3–5 bullet teaser of what's in `ROADMAP.md`, with a link to the full file.
16. **FAQ teaser** — 2–3 of the most common questions inline, link to `docs/FAQ.md` for the rest.
17. **License** — one line ("MIT — see `LICENSE`") plus the badge already shown at the top.
18. **Developer / About** — short bio line: "Built by Jayasubramani (Chip-X, JS SoftTools)" with links to portfolio/GitHub profile.
19. **Support** — how to report bugs (link to Issues + bug report template) and how to request features.
20. **Release / Download** — direct link/button to the latest GitHub Release asset.
21. **Acknowledgements** — credits for third-party libraries used (`tkcalendar`, `Pillow`, PyInstaller) and any assets/icons whose source should be credited.

---

## PHASE 6 — Visual Asset Checklist

| Asset | Filename | Resolution | Aspect Ratio | Background | Stored In | Displayed In |
|---|---|---|---|---|---|---|
| Hero banner | `hero-banner.png` | 1600×400 px | 4:1 | Opaque, dark navy/cyan gradient matching app theme | `assets/banner/` | Top of `README.md` |
| Social preview / OpenGraph image | `social-preview.png` | 1280×640 px | 2:1 | Opaque | `assets/banner/` | GitHub repo Settings → "Social preview" |
| App logo (already exists) | `icon.ico` | 256×256 px (re-export; current file is oversized) | 1:1 | Transparent | `assets/icons/` | README badges area, app taskbar icon |
| Main window screenshot | `main-window.png` | 1280×800 px min | ~16:10 | N/A (real UI capture) | `assets/screenshots/` | README gallery, `docs/USER_GUIDE.md` |
| Add-task modal screenshot | `add-task-modal.png` | 900×700 px min | ~9:7 | N/A | `assets/screenshots/` | README gallery, USER_GUIDE |
| Task detail (readonly) screenshot | `task-detail-view.png` | 900×700 px min | ~9:7 | N/A | `assets/screenshots/` | USER_GUIDE |
| Time Reference view screenshot | `time-reference-view.png` | 1000×700 px min | ~10:7 | N/A | `assets/screenshots/` | README gallery, USER_GUIDE (this is a distinctive/impressive feature worth showcasing prominently) |
| Completed tasks tab screenshot | `completed-tasks-tab.png` | 1280×800 px min | ~16:10 | N/A | `assets/screenshots/` | USER_GUIDE |
| Welcome/splash screenshot | `welcome-screen.png` | 520×600 px (native size) | ~13:15 | N/A | `assets/screenshots/` | README, USER_GUIDE |
| Demo GIF | `demo.gif` | 1000 px wide max | Match capture | N/A | `assets/demo/` | README, embedded inline |
| Demo video | `demo.mp4` | 1920×1080 px | 16:9 | N/A | `assets/demo/` | README (linked/thumbnail), `docs/USER_GUIDE.md` |
| Diagram: DB schema | `db-schema-diagram.png` (or `.svg`) | 1200×900 px | 4:3 | Opaque or transparent | `assets/` (or inline in docs) | `docs/PROJECT_ARCHITECTURE.md` |

**General rules for every screenshot:** dark theme enabled (matches the app's actual only theme), cursor hidden, window sized consistently (~1280×800 for full-window shots), no personal task data visible — populate the app with clearly fictional/demo tasks (e.g., "Buy groceries," "Finish report draft," "Team sync — 3 PM") before capturing anything.

---

## PHASE 7 — Screenshot Detail Specification

| Filename | What appears | Camera/window | Resolution | Cursor visible? | Dark mode? |
|---|---|---|---|---|---|
| `main-window.png` | Full app: folder sidebar, active task list, completed tab visible as a tab | Full app window, no other windows overlapping | 1280×800 | No | Yes (app is dark-only) |
| `add-task-modal.png` | The Add Task modal open with sample fictional data filled in (name, date, notes) | Modal centered, app window behind slightly visible or cropped out | 900×700 | No | Yes |
| `task-detail-view.png` | Read-only task detail view with an attachment and a link listed | Modal only | 900×700 | No | Yes |
| `time-reference-view.png` | The color-coded Time Reference overview (green=good feedback, red=overdue, etc.) with several fictional sample tasks so the color coding is visible | Full Time Reference window | 1000×700 | No | Yes |
| `completed-tasks-tab.png` | Completed tasks list showing a few fictional entries with feedback ratings | Full app window, Completed tab active | 1280×800 | No | Yes |
| `welcome-screen.png` | The neon welcome/splash screen with logo, title, and "Open App" button | Full splash window | 520×600 | No | Yes (native theme) |
| `installer-build-output.png` *(optional)* | Terminal or Desktop showing the built EXE after running the build script | Terminal window or Desktop icon | 1000×600 | Acceptable if showing a click action | N/A |

---

## PHASE 8 — Video Specification

| Video | Length | Scene sequence | Overlays | Music | Ending | Resolution |
|---|---|---|---|---|---|---|
| `demo.gif` (silent, embedded) | 10–20 sec loop | (1) Welcome screen → (2) Main window with folders → (3) Add Task with attachment → (4) Mark complete with feedback | None (GIF has no audio; keep any text overlay minimal since GIFs are heavy) | None | Loops back to welcome screen | 1000 px wide, optimized/compressed |
| `demo.mp4` (full walkthrough) | 60–90 sec | (1) Welcome splash, 3s (2) Main window tour, folders + task list, 10s (3) Add a task + attach a file (image/mp3), 15s (4) Edit a task, 10s (5) Complete a task with feedback rating, 10s (6) Time Reference color-coded view, 15s (7) Completed tab, 8s (8) Closing shot: logo + tagline, 5s | Light text captions per scene (e.g., "Attach any file type") | Optional soft/ambient background track, low volume, royalty-free only | End card with logo, "Star this repo ⭐" call-to-action, GitHub URL | 1920×1080, 30fps |
| `installation.mp4` *(optional, for docs/INSTALL.md)* | 30–45 sec | (1) Download from Releases, 5s (2) Run the EXE, 10s (3) First launch / welcome screen, 10s (4) Ready to use, 10s | Step numbers as on-screen captions | None or very subtle | End on the running app | 1920×1080 |

---

## PHASE 9 — GitHub Presentation Review (Recruiter Lens)

**Current state (before this spec is executed):** a working but unpolished personal-scale repo — functional code, no documentation scaffolding, personal data mixed into what would be committed, 139+38 MB of build artifacts that would bloat clone size dramatically, inconsistent naming, and a bare-bones README.

**Scoring (current → target after full execution):**

| Dimension | Current | Target |
|---|---|---|
| First impression | Weak — no banner, no images, thin README | Strong — banner, badges, GIF demo above the fold |
| Professional score | Low-Medium | High |
| Portfolio score | Low-Medium | High |
| Open-source score | Low (no license, no contribution path, no CI) | High |
| Readability | Medium (code itself is clean; docs are the gap) | High |
| Maintainability | Medium | High (CHANGELOG, ROADMAP, CI in place) |
| Trust | Low (personal data risk, dead files, no license) | High |
| Design quality | Medium (UI itself is genuinely good — neon dark theme) | High (showcased properly via screenshots/GIF) |
| Documentation quality | Low | High |
| User experience (repo navigation) | Low (flat structure, everything mixed) | High (clear `src/`, `docs/`, `assets/` separation) |

**What makes a repository impressive to reviewers from companies like the ones named in this request:** (1) the README answers "what is this and why should I care" in under 10 seconds via a banner + tagline + GIF; (2) the repo is clean at a glance — no build artifacts, no stray files, no dead references; (3) documentation depth signals the author thinks about maintainability, not just "does it run on my machine"; (4) visible CI (a green checkmark) signals the project is verified automatically, not just claimed to work; (5) a proper license and security policy signal the author understands real-world software practices, not just hobbyist scripting; (6) consistent naming and branding throughout (this project already has strong, consistent visual branding — that's an asset to lean into, not rebuild).

---

## PHASE 10 — LinkedIn Preparation Checklist (No Post Written)

**Screenshots needed:** main window, Time Reference color-coded view (most visually distinctive feature), add-task-with-attachment flow, the neon welcome screen (strong branding shot).

**Statistics to include:** total lines of application code (~1,335 across `todo_app.py` + `welcome.py`), number of distinct features (folders, tasks, attachments, links, daily-repeat automation, feedback ratings, Time Reference view — 6+), fully offline/local-first architecture, supported attachment types (any file type — audio, image, document, spreadsheet).

**Achievements to mention:** built a self-migrating SQLite layer (schema auto-upgrades without wiping existing data), implemented a background "midnight watcher" for automatic daily task duplication, packaged as a standalone Windows EXE via PyInstaller.

**Challenges worth mentioning:** designing a safe DB migration path so older databases don't break when new columns are added; building a custom color-coded overview (Time Reference) that visually distinguishes overdue/completed/terminated tasks at a glance.

**Learning outcomes to highlight:** SQLite schema design and migrations, Tkinter modal/window management at scale, packaging Python apps into distributable Windows executables, structuring a solo project for public/open-source presentation.

**Demo to record:** the same `demo.mp4` from Phase 8, or a shorter 15–20 second cut specifically for LinkedIn's native video player.

**Carousel slide order (if using a slide/image carousel post):** (1) hero/branding slide with app name and tagline, (2) problem statement ("most to-do apps don't handle real files well"), (3) main window screenshot, (4) Time Reference feature screenshot, (5) tech stack summary slide, (6) call-to-action slide with GitHub link/QR code.

**Thumbnail:** the same `hero-banner.png` asset, cropped to LinkedIn's preferred aspect ratio (1.91:1 for link previews, 1:1 or 4:5 for native carousel).

---

## PHASE 11 — GitHub Release Organization

**Naming convention:** `vMAJOR.MINOR.PATCH` tags (e.g., `v1.0.0`), following Semantic Versioning. Release titles: `JS To-Do-List vX.Y.Z`.

**Assets attached to each release:**
- `JS-To-Do-List-vX.Y.Z-windows-x64.exe` — the standalone built executable (this is the "installer" experience for end users, even though it's a single portable EXE rather than a true installer — label it accurately as "Portable Executable," not "Installer," unless an actual Inno Setup/NSIS installer is built later)
- `JS-To-Do-List-vX.Y.Z-source.zip` — a zipped snapshot of the source (GitHub generates this automatically for every release/tag, no manual work needed)
- `SHA256SUMS.txt` — checksums for the `.exe`, so users can verify the download wasn't tampered with

**Release notes structure:** short summary paragraph, then `### Added`, `### Changed`, `### Fixed`, `### Known Issues` sections mirroring the `CHANGELOG.md` entry for that version.

**Versioning policy:** MAJOR for breaking DB schema changes or UI overhauls, MINOR for new features (e.g., new attachment type support), PATCH for bug fixes only. First public release should be tagged `v1.0.0` since the app is already functionally complete — do not artificially start at `v0.1.0` for a working product.

---

## PHASE 12 — Source Code Protection Options

The stated goal: let users freely download and run the **executable**, while preventing casual users from obtaining the **source code**.

| Approach | Advantages | Disadvantages | Professional usage | Recommended? |
|---|---|---|---|---|
| **Public repository (full source)** | Maximum trust, portfolio value, recruiter-friendly, enables community contributions and CI | Anyone can read/copy the source | Extremely common for portfolio/open-source projects | Recommended **if** the goal is portfolio/recruiter visibility (source code is the thing being showcased) |
| **Private repository, releases made public via a separate mechanism** | Source fully hidden | GitHub does not allow attaching Releases visibly to the public from a fully private repo without also making the repo (or at least Releases) visible; largely defeats "share it publicly" | Used by companies for proprietary internal tools | Not recommended if the goal is public sharing of the app |
| **Separate public "releases-only" repository + separate private source repository** | End users get a clean public repo with just the README + downloadable EXE via Releases; real source stays in a private repo | Two repos to maintain; the public one has no code to showcase to recruiters (defeats the portfolio goal in this exact request) | Common pattern for commercial software vendors distributing free binaries | Only recommended if source-hiding is prioritized over portfolio/recruiter visibility — **conflicts with the stated goal of this spec** |
| **GitHub Releases only (source repo stays public, but README emphasizes "Releases" for casual users)** | Casual/non-technical users naturally gravitate to the green "Download" via Releases rather than browsing source; source remains visible for recruiters/technical reviewers who look for it | Does not actually hide source from anyone who clicks "Code" | Extremely common — most open-source desktop apps work exactly this way | **Recommended** — matches both stated goals (easy EXE download + portfolio visibility) simultaneously |
| **External website for distribution (e.g., itch.io, personal site, Netlify-hosted download page)** | Casual users never see a "Code" tab at all; feels like a polished product page | Extra infrastructure to maintain; still doesn't hide the source if the GitHub repo backing it is public | Common for indie software/games | Optional addition on top of the GitHub-Releases approach, not a replacement |
| **Cloud storage (Google Drive/Dropbox link) for the EXE** | Zero GitHub Release setup needed | Looks unprofessional compared to GitHub Releases; no version history, no checksums, easily goes stale | Not used by any professional or reputable open-source project | Not recommended |
| **License-based protection (e.g., "All Rights Reserved" or a restrictive custom license) while still keeping source public** | Legally prevents redistribution/reuse even though the code is visible | Does not technically hide anything; only creates legal recourse after the fact | Common for "source-available but not open-source" projects | Optional layer, can combine with the public-repo approach — does not achieve technical hiding, only legal protection |
| **Executable/code obfuscation (PyArmor, Nuitka, PyInstaller + obfuscation) applied only to the shipped `.exe`** | Makes reverse-engineering the compiled binary harder for casual users, while source in the repo stays fully readable for legitimate purposes | Does not prevent someone from simply reading the public GitHub source directly — irrelevant if the repo itself is public | Common in commercial software distribution | Irrelevant to this specific goal since the repo would still show the raw `.py` source; only useful if combined with a private-source approach |
| **Repository split by file sensitivity (keep `.spec`/build config private, source public)** | Marginal — doesn't really apply here since there's no sensitive build secret in this project (no API keys, no credentials found in inspection) | N/A | N/A | Not applicable — no secrets were found in this codebase during inspection |

**Recommended approach for this specific project:** Keep the repository fully public (source visible) and rely on the README/Releases structure so casual, non-technical users naturally use the "Download the `.exe` from Releases" path while the source remains visible to recruiters and technical reviewers — which directly serves the stated goal of this entire specification (a portfolio-quality public repository). True source-hiding (private repo, separate distribution site) is technically possible but **directly contradicts** the goal of having "Microsoft, Google, Amazon, NVIDIA, OpenAI, and thousands of GitHub developers" review this as a portfolio project, since none of them can review source they cannot see. If source-hiding is truly a hard requirement for a *future* commercial version of this app, that would need to be a separate, differently-scoped project decision — not applied to the portfolio repository this specification is building.

---

## PHASE 13 — Implementation Master Plan (Numbered, For an Executing AI)

### Phase 13.1 — Cleanup & Sanitization
**Objective:** Remove all dead files, duplicates, personal data, and build artifacts before any repo structure is created.
**Files to remove:** `build_app.bat.txt`, `notify.vbs.txt`, `main.spec`, `dist/js_todo.db`, `data/` (folder), `task_attachments/tasks.txt`, entire `outputs/` folder, entire `build/` folder, entire `dist/` folder, `js_todo.db` (real data — replace per 13.2).
**Folders to remove:** `build/`, `dist/`, `outputs/`, `data/`, all of `task_attachments/`'s existing personal subfolders (`f1_t4`, `f1_t7`, `f21_t3`, `f7_t1`).
**Verification checklist:** confirm no file under 500 KB total remains referencing personal task names/dates; confirm `main.py` is genuinely absent (so deleting `main.spec` is safe); confirm `todo_app.py` still imports/runs identically after removals (removals only touch non-source files).
**Estimated time:** 15 minutes. **Difficulty:** Trivial. **Dependencies:** None.
**Expected output:** a clean working directory with only source, packaging configs, and the icon remaining.

### Phase 13.2 — Personal Data Scrub
**Objective:** Ensure zero personal data ships in the public repo while keeping the app runnable out of the box.
**Files to create:** optionally `sample_data/demo_seed.db` — a freshly initialized SQLite DB (run `init_db()` once, then insert 3–4 clearly fictional tasks such as "Buy groceries," "Finish quarterly report," "Team standup — 9 AM").
**Files to modify:** none required in `todo_app.py` itself — the existing code already calls `os.makedirs(ATTACHMENT_DIR, exist_ok=True)` and creates the DB file automatically if absent, so a first-time clone-and-run experience already works without any personal file being present.
**Verification checklist:** delete the real `js_todo.db`, run `todo_app.py` fresh, confirm it recreates an empty DB with the three special folders (Daily Habit, Health Care, Time Reference) intact via `init_db()`.
**Estimated time:** 20 minutes. **Difficulty:** Easy. **Dependencies:** Phase 13.1 complete.
**Expected output:** the app runs standalone with zero pre-existing personal data.

### Phase 13.3 — Path Portability Fix
**Objective:** Remove hardcoded developer-machine absolute paths so the project builds on any machine.
**Files to modify:**
- `welcome.spec` — change `'E:\\Chip-X\\JS To-Do-List\\To-Do-List\\welcome.py'` to a relative path (`'welcome.py'`, assuming the spec lives alongside the source, or `'../src/welcome.py'` once moved into `packaging/`), and change `icon=['E:\\DEVELPOMENT files\\To-Do-List\\icon.ico']` to `icon=['../assets/icons/icon.ico']`.
- `welcome.py` — change the hardcoded `logo_path = r"E:\DEVELPOMENT files\To-Do-List\icon.ico"` and `exe_path = r"E:\DEVELPOMENT files\To-Do-List\outputs\JS To-Do List.exe"` to paths computed relative to the script's own location (mirroring the `BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))` pattern already correctly used in `todo_app.py`).
**Verification checklist:** confirm `welcome.py` and its `.spec` contain zero occurrences of `E:\` or any absolute path; confirm the welcome screen still locates and displays the logo, and the "Open App" button still finds the built executable, when run from a fresh clone on a different machine/drive letter.
**Estimated time:** 20 minutes. **Difficulty:** Easy. **Dependencies:** None (can run in parallel with 13.1).
**Expected output:** fully portable build configuration and launcher script.

### Phase 13.4 — Repository Restructure
**Objective:** Reorganize the sanitized project into the Phase 2 folder structure.
**Folders to create:** `.github/ISSUE_TEMPLATE/`, `.github/workflows/`, `assets/icons/`, `assets/screenshots/`, `assets/banner/`, `assets/demo/`, `docs/`, `src/`, `packaging/`, `sample_data/` (if using 13.2's optional seed DB).
**Files to move:** `todo_app.py` → `src/todo_app.py`; `welcome.py` → `src/welcome.py`; `todo_app.spec` → `packaging/todo_app.spec`; `welcome.spec` → `packaging/welcome.spec`; `build_app.bat` → `packaging/build_app.bat`; `icon.ico` → `assets/icons/icon.ico`.
**Files to modify:** update path references inside the moved `.spec` files and `build_app.bat` to reflect new relative locations (e.g., `--icon=../assets/icons/icon.ico` if invoked from `packaging/`).
**Verification checklist:** run the build script from its new location and confirm it still produces a working EXE with the correct icon; confirm `src/todo_app.py` still runs standalone with `python src/todo_app.py` from the repo root (may require adjusting the working-directory assumption for `DB_PATH`/`ATTACHMENT_DIR`, which currently assume the current working directory — document this clearly in `docs/BUILD.md` rather than silently changing app behavior, per the "do not change functionality" constraint).
**Estimated time:** 30–45 minutes. **Difficulty:** Moderate (path reference updates need care). **Dependencies:** Phases 13.1–13.3 complete.
**Expected output:** the full Phase 2 folder tree, populated and functional.

### Phase 13.5 — Core Documentation & Legal Files
**Objective:** Create every file listed in Phase 4.
**Files to create:** `LICENSE`, `CHANGELOG.md`, `ROADMAP.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `DISCLAIMER.md`, `VERSION`, `.gitignore`, `requirements.txt`, `docs/INSTALL.md`, `docs/USER_GUIDE.md`, `docs/BUILD.md`, `docs/PROJECT_ARCHITECTURE.md`, `docs/FEATURES.md`, `docs/FAQ.md`, `docs/KNOWN_ISSUES.md`.
**Verification checklist:** every file listed in Phase 4's table exists at the correct path; `.gitignore` correctly excludes `build/`, `dist/`, `__pycache__/`, `*.pyc`, `js_todo.db`, `task_attachments/` (the real one, not `sample_data/`), `outputs/`; `requirements.txt` installs cleanly into a fresh virtual environment and successfully runs `src/todo_app.py`.
**Estimated time:** 3–5 hours (writing quality documentation takes real time). **Difficulty:** Moderate. **Dependencies:** Phase 13.4 complete (needs final folder paths to reference correctly).
**Expected output:** a fully documented repository meeting GitHub's "Community Standards" checklist at 100%.

### Phase 13.6 — GitHub Automation
**Objective:** Add issue/PR templates and CI/CD workflows.
**Files to create:** `.github/ISSUE_TEMPLATE/bug_report.md`, `.github/ISSUE_TEMPLATE/feature_request.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/workflows/build-windows.yml`, `.github/workflows/release.yml`.
**Verification checklist:** push a test commit and confirm `build-windows.yml` runs and turns green; push a test tag (e.g., `v0.0.1-test`) and confirm `release.yml` successfully attaches a built EXE to a draft release; delete the test tag/release afterward.
**Estimated time:** 2–3 hours (YAML debugging typically takes iteration). **Difficulty:** Moderate-High. **Dependencies:** Phase 13.4 complete (workflow paths must match final `src/`/`packaging/` locations).
**Expected output:** working CI badge for the README and one-click automated releases going forward.

### Phase 13.7 — Visual Asset Production
**Objective:** Produce every asset listed in Phases 6–8.
**Assets to create:** hero banner, social preview image, all 7 screenshots, demo GIF, demo MP4, optional DB schema diagram.
**Verification checklist:** every filename matches exactly what Phase 6's table and the README (Phase 13.8) reference; all screenshots show only fictional demo data (cross-check against Phase 13.2's seed data); GIF file size is reasonable for embedding (under ~10 MB recommended); social preview image is uploaded to the repo's Settings page in addition to being stored in `assets/`.
**Estimated time:** 3–6 hours (screen recording, editing, and export take the most real time in this entire plan). **Difficulty:** Moderate (production work, not technical difficulty). **Dependencies:** Phase 13.2 (needs clean demo data) and Phase 13.4 (needs final UI, unchanged from original since no functionality changes).
**Expected output:** the complete `assets/` folder populated per the Phase 6 table.

### Phase 13.8 — README Assembly
**Objective:** Write the final `README.md` following the exact Phase 5 section order, embedding the Phase 13.7 assets and linking to the Phase 13.5 docs.
**Files to modify:** `README.md` (full rewrite, replacing the current 66-line version).
**Verification checklist:** every section from Phase 5's 21-item list is present in order; every image reference resolves to an actual file in `assets/`; every internal link (`docs/...`) resolves to a real file; badges render correctly (test by previewing the rendered Markdown on GitHub).
**Estimated time:** 2–3 hours. **Difficulty:** Moderate. **Dependencies:** Phases 13.5, 13.6, 13.7 all complete (README references all of them).
**Expected output:** a complete, polished, professional README matching the blueprint.

### Phase 13.9 — First Public Release
**Objective:** Cut the first official `v1.0.0` release per Phase 11's conventions.
**Steps:** update `VERSION` to `1.0.0`, add the corresponding `v1.0.0` entry to `CHANGELOG.md`, tag the commit `v1.0.0`, let `release.yml` (Phase 13.6) build and attach `JS-To-Do-List-v1.0.0-windows-x64.exe` plus a generated `SHA256SUMS.txt`, write release notes mirroring the changelog entry.
**Verification checklist:** the Release page shows the correct asset names per Phase 11's naming convention; the downloaded EXE actually launches on a clean Windows machine with no Python installed; checksums match.
**Estimated time:** 30–60 minutes (mostly automated once 13.6 works). **Difficulty:** Easy. **Dependencies:** Phases 13.6 and 13.8 complete.
**Expected output:** a public, downloadable, versioned release — the final deliverable of this entire specification.

### Phase 13.10 — Final Quality Pass
**Objective:** Verify the repository against the Phase 9 scoring rubric before considering the transformation complete.
**Verification checklist:** re-run through every item in Phase 9's "Target" column and confirm it is genuinely met; confirm zero personal data anywhere in git history (not just the working tree — if personal data was ever committed during development, the git history itself must be scrubbed, e.g., via a fresh repository init rather than `git filter-branch` band-aids); confirm repository size is dramatically smaller than the original 191 MB working folder (expect well under 5 MB for source + docs, with binaries living only in Releases); confirm GitHub's "Community Standards" checklist (Insights tab) shows 100%.
**Estimated time:** 1 hour. **Difficulty:** Easy. **Dependencies:** All prior phases complete.
**Expected output:** a repository ready to be linked from a resume, portfolio site, or LinkedIn profile with full confidence.

---

## Summary Table — Total Effort Estimate

| Phase | Estimated Time |
|---|---|
| 13.1 Cleanup & Sanitization | 15 min |
| 13.2 Personal Data Scrub | 20 min |
| 13.3 Path Portability Fix | 20 min |
| 13.4 Repository Restructure | 30–45 min |
| 13.5 Core Documentation & Legal Files | 3–5 hrs |
| 13.6 GitHub Automation | 2–3 hrs |
| 13.7 Visual Asset Production | 3–6 hrs |
| 13.8 README Assembly | 2–3 hrs |
| 13.9 First Public Release | 30–60 min |
| 13.10 Final Quality Pass | 1 hr |
| **Total** | **~13–20 hours** |

This specification is now complete and ready to be handed to a coding AI (or executed manually) to perform the actual file operations, documentation writing, and asset production.
