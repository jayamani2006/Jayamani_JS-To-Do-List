# JS To-Do-List Installation Guide

The application is distributed as a professional Windows installer. You do not need to install Python or run any complicated setup commands.

## Installation Steps
1. Download the installer executable (`JS_ToDo_Setup.exe`) from the [Latest Release](https://github.com/jayamani2006/Jayamani_JS-To-Do-List/releases/latest) page.
2. Run the installer and choose your preferred installation location.
3. Complete the installation. The installer will automatically extract and configure the required application folder.

---

## Installation Location
During installation, the setup wizard will ask where to install the application. For the best experience and data safety, install the application into its own dedicated folder directly at the root of a drive.

**Recommended installation locations:**
- ✔ `D:\JS To-Do-List`
- ✔ `E:\JS To-Do-List`

**If your computer only has a C drive:**
- ✔ `C:\JS To-Do-List`

**Avoid installing inside these locations:**
- ❌ `C:\Program Files`
- ❌ `C:\Program Files (x86)`
- ❌ Windows System folders
- ❌ Desktop
- ❌ Downloads
- ❌ Deeply nested folders (e.g. `C:\Users\User\Downloads\New Folder\Another Folder\JS To-Do-List`)

> **Why?** Keeping the application folder at the root level of the drive prevents Windows permissions issues with the local SQLite database.
