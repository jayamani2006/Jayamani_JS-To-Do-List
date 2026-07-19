# Project Architecture

JS To-Do-List is built entirely using Python and Tkinter, with SQLite acting as the robust local data layer.

## Database Schema

The core database `js_todo.db` consists of four primary tables:

1. **folders:** Stores custom folders (`id`, `name`, `is_special`).
2. **tasks:** Stores all tasks (`id`, `folder_id`, `name`, `due_date`, `due_time`, `notes`, `status`, `feedback`, `feedback_comment`).
3. **task_attachments:** Links files to tasks (`id`, `task_id`, `file_path`, `original_name`).
4. **task_links:** Links URLs to tasks (`id`, `task_id`, `url`).

### Automatic Migrations

The `init_db()` function serves as an auto-migration layer. It safely adds missing columns for older schema versions to prevent `sqlite3.OperationalError` from breaking older local databases.

## Application State

The UI heavily relies on a decoupled class structure:
- **TodoApp:** The main application window and logic controller.
- **TaskModal:** The dedicated UI for adding, viewing, and editing tasks.
- **Welcome:** A separate `welcome.py` launcher with a neon splash screen.

## Midnight Watcher

The application uses an internal background loop utilizing `after()` to monitor the system clock. When the clock strikes midnight, it automatically duplicates uncompleted tasks in the `Daily Habit` and `Health Care` folders to enforce daily tracking.
