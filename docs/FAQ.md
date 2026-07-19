# Frequently Asked Questions (FAQ)

### Where are my attachments stored?
When you attach a file to a task, a copy of the file is created locally inside the `task_attachments/` folder. This means even if you delete the original file on your computer, your task will still have access to the attached copy.

### Is my data sent anywhere?
No. JS To-Do-List is 100% offline. Your data is stored strictly in the local `js_todo.db` SQLite database on your machine.

### Can I use this on macOS or Linux?
Currently, the pre-built executables are for Windows 10/11 only. However, you can run the source code directly on macOS or Linux using Python.

### How do I backup my tasks?
Simply copy the `js_todo.db` file and the `task_attachments/` folder to a safe location. To restore, paste them back into the application's root directory.
