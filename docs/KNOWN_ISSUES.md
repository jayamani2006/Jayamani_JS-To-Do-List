# Known Issues & Limitations

- **Windows-only executable:** The compiled release binary is strictly for Windows. Mac and Linux users must run from source.
- **No cloud backup:** Data is entirely local. You are responsible for backing up your `js_todo.db` and `task_attachments/` directories.
- **Large attachments:** Because attachments are physically copied into `task_attachments/`, attaching extremely large files (e.g., 2GB videos) will linearly increase the storage size of your app directory.
- **No keyboard navigation:** The UI is currently fully mouse-driven. Enhanced keyboard shortcut support is on the roadmap.
