#!/usr/bin/env python3
"""
JS To-Do-List - single-file app (fixed & migrated)

Save as todo_app.py and run with Python 3.8+.

Dependencies:
    pip install tkcalendar pillow

Features:
 - Folder system (scrollable)
 - Special bottom folder actions: Daily Habit, Health Care, Time Reference
 
 - Add/Edit/View tasks: name, due date, due time, notes
 - Attachments saved under ATTACHMENT_DIR/<folder_prefix>_t<taskid>
 - Attachments preview/open/delete (available in all modes)
 - Links add/open/delete (available in all modes)
 - Completion & feedback (Perfect/Good/Average/Poor/Other with comment)
 - Terminate (mark as terminated and move to completed)
 - Daily auto-duplicate for repeat_daily tasks in Daily Habit & Health Care
 - Scrollable modals, combobox scrolling isolation
 - Dark theme (black/blue), larger fonts
 - SQLite DB with migration (adds missing columns safely)
"""

import os
import sqlite3
import shutil
import webbrowser
import sys
from datetime import datetime, date, timedelta
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkcalendar import Calendar
from PIL import Image, ImageTk

# --- Base directory (works for .exe and .py) ---
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# --- Folders used by your app ---
FOLDERS = ["task_attachments", "data"]  # add more folder names if needed

# --- Create folders safely ---
for folder in FOLDERS:
    folder_path = os.path.join(BASE_DIR, folder)
    try:
        os.makedirs(folder_path, exist_ok=True)
    except PermissionError:
        print(f"Cannot create folder: {folder_path}")
        sys.exit(1)

# --- Example usage ---
task_file = os.path.join(BASE_DIR, "task_attachments", "tasks.txt")
if not os.path.exists(task_file):
    with open(task_file, "w") as f:
        f.write("")  # creates an empty tasks file

# --- Your existing main.py code continues below ---


APP_NAME = "JS To-Do-List"
DB_PATH = "js_todo.db"
ATTACHMENT_DIR = "task_attachments"

# UI scale
FONT_SCALE = 1.4
FONT_NAME = ("Helvetica", int(10 * FONT_SCALE))

os.makedirs(ATTACHMENT_DIR, exist_ok=True)

# -------------------------
# Database helpers & migration
# -------------------------
def get_conn():
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    return conn

def _table_columns(conn, table):
    cur = conn.execute(f"PRAGMA table_info({table})")
    return [r["name"] for r in cur.fetchall()]

def init_db():
    """
    Create tables if missing and perform migrations (add missing columns).
    This avoids 'table has no column' errors on older DBs.
    """
    conn = get_conn()
    cur = conn.cursor()

    # Create folders table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS folders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        is_special INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # Create tasks table with full schema (some older DBs may lack columns)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        folder_id INTEGER,
        name TEXT NOT NULL,
        due_date TEXT,
        due_time TEXT,
        notes TEXT,
        repeat_daily INTEGER DEFAULT 0,
        completed INTEGER DEFAULT 0,
        terminated INTEGER DEFAULT 0,
        completed_at TEXT,
        feedback TEXT,
        feedback_comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(folder_id) REFERENCES folders(id) ON DELETE SET NULL
    )""")

    # Create attachments & links
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attachments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        file_name TEXT,
        file_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS task_links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        name TEXT,
        url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
    )""")
    conn.commit()

    # Migration safety: Ensure columns exist in tasks (if DB was older)
    existing = _table_columns(conn, "tasks")
    col_adds = []
    expected_cols = {
        "folder_id": "ALTER TABLE tasks ADD COLUMN folder_id INTEGER DEFAULT NULL",
        "repeat_daily": "ALTER TABLE tasks ADD COLUMN repeat_daily INTEGER DEFAULT 0",
        "terminated": "ALTER TABLE tasks ADD COLUMN terminated INTEGER DEFAULT 0",
        "completed_at": "ALTER TABLE tasks ADD COLUMN completed_at TEXT",
        "feedback": "ALTER TABLE tasks ADD COLUMN feedback TEXT",
        "feedback_comment": "ALTER TABLE tasks ADD COLUMN feedback_comment TEXT"
    }
    for col, stmt in expected_cols.items():
        if col not in existing:
            try:
                cur.execute(stmt)
                col_adds.append(col)
            except sqlite3.OperationalError:
                pass
    conn.commit()

    # ensure special folders exist
    specials = [("Daily Habit",1), ("Health Care",1), ("Time Reference",1)]
    for name, is_special in specials:
        try:
            cur.execute("INSERT OR IGNORE INTO folders(name,is_special) VALUES(?,?)", (name, is_special))
        except Exception:
            pass
    conn.commit()
    conn.close()

# -------------------------
# Folder functions
# -------------------------
def fetch_folders():
    conn = get_conn()
    cur = conn.execute("SELECT * FROM folders ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_folder(name):
    conn = get_conn()
    cur = conn.execute("INSERT INTO folders(name) VALUES(?)", (name.strip(),))
    fid = cur.lastrowid
    conn.commit()
    conn.close()
    return fid

def rename_folder(folder_id, new_name):
    conn = get_conn()
    conn.execute("UPDATE folders SET name=? WHERE id=?", (new_name.strip(), folder_id))
    conn.commit()
    conn.close()

def delete_folder(folder_id):
    # remove attachment files too
    conn = get_conn()
    cur = conn.execute("SELECT id FROM tasks WHERE folder_id=?", (folder_id,))
    tasks = cur.fetchall()
    for t in tasks:
        delete_task(t["id"])
    conn.execute("DELETE FROM folders WHERE id=?", (folder_id,))
    conn.commit()
    conn.close()

# -------------------------
# Task functions
# -------------------------
def add_task(name, date_str, time_str, notes, folder_id=None, repeat_daily=0):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO tasks(folder_id,name,due_date,due_time,notes,repeat_daily) VALUES(?,?,?,?,?,?)",
        (folder_id, name, date_str, time_str, notes, repeat_daily)
    )
    tid = cur.lastrowid
    conn.commit()
    conn.close()
    return tid

def update_task(task_id, name, date_str, time_str, notes, folder_id=None, repeat_daily=0):
    conn = get_conn()
    conn.execute(
        "UPDATE tasks SET name=?, due_date=?, due_time=?, notes=?, folder_id=?, repeat_daily=? WHERE id=?",
        (name, date_str, time_str, notes, folder_id, repeat_daily, task_id)
    )
    conn.commit()
    conn.close()

def delete_task(task_id):
    # remove attachment files too
    conn = get_conn()
    cur = conn.execute("SELECT file_path FROM attachments WHERE task_id=?", (task_id,))
    rows = cur.fetchall()
    for r in rows:
        p = r["file_path"]
        try:
            if os.path.exists(p):
                os.remove(p)
        except:
            pass
    conn.execute("DELETE FROM attachments WHERE task_id=?", (task_id,))
    conn.execute("DELETE FROM task_links WHERE task_id=?", (task_id,))
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def complete_task_with_feedback(task_id, feedback, comment=None, terminated=False):
    conn = get_conn()
    now = datetime.now().strftime("%d-%b-%Y %I:%M %p")
    if terminated:
        conn.execute(
            "UPDATE tasks SET completed=1, terminated=1, completed_at=?, feedback=?, feedback_comment=? WHERE id=?",
            (now, feedback, comment, task_id)
        )
    else:
        conn.execute(
            "UPDATE tasks SET completed=1, completed_at=?, feedback=?, feedback_comment=? WHERE id=?",
            (now, feedback, comment, task_id)
        )
    conn.commit()
    conn.close()

def fetch_tasks(completed=0, folder_id=None):
    conn = get_conn()
    if folder_id is None:
        cur = conn.execute("SELECT * FROM tasks WHERE completed=? ORDER BY due_date,due_time", (completed,))
    else:
        cur = conn.execute("SELECT * FROM tasks WHERE completed=? AND folder_id=? ORDER BY due_date,due_time", (completed, folder_id))
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_task_by_id(task_id):
    conn = get_conn()
    cur = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    r = cur.fetchone()
    conn.close()
    return r

# -------------------------
# Attachments & Links
# -------------------------
def save_attachment_db(task_id, src_path):
    task = fetch_task_by_id(task_id)
    folder_id = task["folder_id"] if task else None
    folder_prefix = f"nofolder" if folder_id is None else f"f{folder_id}"
    dest_dir = os.path.join(ATTACHMENT_DIR, f"{folder_prefix}_t{task_id}")
    os.makedirs(dest_dir, exist_ok=True)
    base = os.path.basename(src_path)
    dest = os.path.join(dest_dir, base)
    name, ext = os.path.splitext(dest)
    i = 1
    while os.path.exists(dest):
        dest = f"{name}_{i}{ext}"
        i += 1
    try:
        shutil.copy2(src_path, dest)
    except Exception:
        # fallback to referencing original
        dest = src_path
    conn = get_conn()
    conn.execute("INSERT INTO attachments(task_id, file_name, file_path) VALUES(?,?,?)",
                 (task_id, os.path.basename(dest), os.path.abspath(dest)))
    conn.commit()
    conn.close()
    return dest

def fetch_attachments(task_id):
    conn = get_conn()
    cur = conn.execute("SELECT * FROM attachments WHERE task_id=?", (task_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_attachment_db(att_id):
    conn = get_conn()
    cur = conn.execute("SELECT file_path FROM attachments WHERE id=?", (att_id,))
    r = cur.fetchone()
    if r:
        p = r["file_path"]
        try:
            if os.path.exists(p):
                os.remove(p)
        except:
            pass
    conn.execute("DELETE FROM attachments WHERE id=?", (att_id,))
    conn.commit()
    conn.close()

def save_task_link_db(task_id, name, url):
    conn = get_conn()
    cur = conn.execute("INSERT INTO task_links(task_id,name,url) VALUES(?,?,?)", (task_id, name.strip(), url.strip()))
    conn.commit()
    lid = cur.lastrowid
    conn.close()
    return lid

def fetch_task_links(task_id):
    conn = get_conn()
    cur = conn.execute("SELECT * FROM task_links WHERE task_id=?", (task_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_task_link_db(link_id):
    conn = get_conn()
    conn.execute("DELETE FROM task_links WHERE id=?", (link_id,))
    conn.commit()
    conn.close()

# -------------------------
# Utilities
# -------------------------
def safe_open(path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform.startswith("darwin"):
            os.system(f'open "{path}"')
        else:
            webbrowser.open(path)
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open file: {e}")

# -------------------------
# Duplicate daily tasks for date
# -------------------------
def duplicate_daily_tasks_for_date(target_date):
    conn = get_conn()
    cur = conn.execute("SELECT id,name FROM folders WHERE name IN ('Daily Habit','Health Care')")
    special = cur.fetchall()
    special_ids = [s["id"] for s in special]
    for fid in special_ids:
        rows = conn.execute("SELECT * FROM tasks WHERE folder_id=? AND repeat_daily=1", (fid,)).fetchall()
        for r in rows:
            # Avoid duplicating if already duplicated for that date (simple check)
            existing = conn.execute("SELECT id FROM tasks WHERE folder_id=? AND due_date=? AND name=?", (fid, target_date.isoformat(), r["name"])).fetchone()
            if existing:
                continue
            new_tid = add_task(r["name"], target_date.isoformat(), r["due_time"], r["notes"], folder_id=fid, repeat_daily=1)
            atts = fetch_attachments(r["id"])
            for a in atts:
                src = a["file_path"]
                try:
                    save_attachment_db(new_tid, src)
                except Exception:
                    # fallback: insert reference
                    conn2 = get_conn()
                    conn2.execute("INSERT INTO attachments(task_id,file_name,file_path) VALUES(?,?,?)", (new_tid, a["file_name"], a["file_path"]))
                    conn2.commit()
                    conn2.close()
            links = fetch_task_links(r["id"])
            for lk in links:
                save_task_link_db(new_tid, lk["name"], lk["url"])
    conn.close()

# -------------------------
# GUI components
# -------------------------
class TaskModal(tk.Toplevel):
    def __init__(self, master, title, task=None, readonly=False, default_folder_id=None):
        super().__init__(master)
        self.master = master
        self.task = task
        self.readonly = readonly
        self.default_folder_id = default_folder_id
        self.attachments_local = []   # absolute paths (DB or newly chosen)
        self.db_attachments = []      # DB rows
        self.links_new = []
        self.links_db = []
        self.title(title)
        self.configure(bg="#0b1220")
        self.geometry("920x760")
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Scrollable canvas
        self.canvas = tk.Canvas(self, bg="#0b1220", highlightthickness=0)
        self.vscroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas, bg="#0b1220")
        self.canvas_win = self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vscroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vscroll.pack(side="right", fill="y")
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_win, width=e.width))

        # mouse wheel bindings while pointer inside canvas
        self.canvas.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())

        # Build
        self._build_widgets()

        # Load attachments & links from DB if editing/viewing
        if self.task:
            atts = fetch_attachments(self.task["id"])
            for a in atts:
                self.db_attachments.append(a)
                self.attachments_local.append(a["file_path"])
                self.att_listbox.insert(tk.END, a["file_name"])
            lks = fetch_task_links(self.task["id"])
            for lk in lks:
                self.links_db.append(lk)
                self.link_listbox.insert(tk.END, f"{lk['name']} | {lk['url']}")

        # Ensure combobox dropdown doesn't scroll page
        self._hook_combobox_scroll(self.hour_cb)
        self._hook_combobox_scroll(self.min_cb)
        self._hook_combobox_scroll(self.ampm_cb)

    def _bind_mousewheel(self):
        if sys.platform == "darwin":
            self.bind_all("<MouseWheel>", self._on_mousewheel)
        else:
            self.bind_all("<MouseWheel>", self._on_mousewheel)
            self.bind_all("<Button-4>", self._on_mousewheel)
            self.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self):
        try:
            self.unbind_all("<MouseWheel>")
            self.unbind_all("<Button-4>")
            self.unbind_all("<Button-5>")
        except:
            pass

    def _on_mousewheel(self, ev):
        if hasattr(ev, "delta") and ev.delta:
            self.canvas.yview_scroll(int(-1 * (ev.delta/120)), "units")
        else:
            if getattr(ev, "num", None) == 4:
                self.canvas.yview_scroll(-1, "units")
            elif getattr(ev, "num", None) == 5:
                self.canvas.yview_scroll(1, "units")

    def _hook_combobox_scroll(self, cb):
        def on_focus_in(e):
            self._unbind_mousewheel()
        def on_focus_out(e):
            self._bind_mousewheel()
        cb.bind("<FocusIn>", on_focus_in)
        cb.bind("<FocusOut>", on_focus_out)

    def _build_widgets(self):
        padx = 16
        sf = self.frame
        tk.Label(sf, text=self.title(), font=(FONT_NAME[0], int(14*FONT_SCALE), "bold"), bg="#0b1220", fg="#cfe8ff").pack(pady=10)
        # folders
        folders = fetch_folders()
        self.folder_map = [(f["id"], f["name"]) for f in folders]
        names = [n for (_i,n) in self.folder_map]
        self.folder_var = tk.StringVar()
        self.folder_cb = ttk.Combobox(sf, values=names, textvariable=self.folder_var, state="readonly", width=36)
        if self.task and self.task["folder_id"]:
            for fid, fname in self.folder_map:
                if fid == self.task["folder_id"]:
                    self.folder_var.set(fname)
                    break
        elif self.default_folder_id:
            for fid, fname in self.folder_map:
                if fid == self.default_folder_id:
                    self.folder_var.set(fname)
                    break
        elif names:
            self.folder_var.set(names[0])
        self.folder_cb.pack(padx=padx, pady=6, anchor="w")
        # name
        tk.Label(sf, text="Task Name:", bg="#0b1220", fg="#cfe8ff", font=FONT_NAME).pack(anchor="w", padx=padx)
        self.name_entry = tk.Entry(sf, width=64, font=FONT_NAME)
        self.name_entry.pack(padx=padx, pady=6, anchor="w")
        if self.task:
            self.name_entry.insert(0, self.task["name"])
        if self.readonly:
            self.name_entry.configure(state="readonly")
        # date
        tk.Label(sf, text="Due Date:", bg="#0b1220", fg="#cfe8ff", font=FONT_NAME).pack(anchor="w", padx=padx)
        self.cal = Calendar(sf)
        self.cal.pack(padx=padx, pady=6, anchor="w")
        if self.task and self.task["due_date"]:
            try:
                self.cal.set_date(self.task["due_date"])
            except:
                pass
        # time picker
        tk.Label(sf, text="Due Time:", bg="#0b1220", fg="#cfe8ff", font=FONT_NAME).pack(anchor="w", padx=padx)
        time_frame = tk.Frame(sf, bg="#0b1220")
        time_frame.pack(anchor="w", padx=padx, pady=6)
        hours = [f"{i:02}" for i in range(1,13)]
        minutes = [f"{i:02}" for i in range(0,60)]
        ampm = ["AM", "PM"]
        self.hour_var = tk.StringVar(value=hours[0])
        self.min_var = tk.StringVar(value=minutes[0])
        self.ampm_var = tk.StringVar(value=ampm[0])
        self.hour_cb = ttk.Combobox(time_frame, values=hours, width=6, textvariable=self.hour_var, state="readonly")
        self.min_cb = ttk.Combobox(time_frame, values=minutes, width=6, textvariable=self.min_var, state="readonly")
        self.ampm_cb = ttk.Combobox(time_frame, values=ampm, width=6, textvariable=self.ampm_var, state="readonly")
        self.hour_cb.pack(side="left")
        tk.Label(time_frame, text=":", bg="#0b1220", fg="#cfe8ff").pack(side="left", padx=4)
        self.min_cb.pack(side="left", padx=(0,6))
        self.ampm_cb.pack(side="left")
        if self.task and self.task["due_time"]:
            try:
                tparts = self.task["due_time"].split()
                hm = tparts[0].split(":")
                self.hour_var.set(hm[0]); self.min_var.set(hm[1]); self.ampm_var.set(tparts[1])
            except:
                pass
        if self.readonly:
            self.hour_cb.config(state="disabled"); self.min_cb.config(state="disabled"); self.ampm_cb.config(state="disabled")
        # repeat daily
        self.repeat_var = tk.IntVar(value=1 if (self.task and self.task["repeat_daily"]) else 0)
        tk.Checkbutton(sf, text="Repeat Daily (duplicate at midnight)", variable=self.repeat_var, bg="#0b1220", fg="#cfe8ff", selectcolor="#073642", font=FONT_NAME, activebackground="#0b1220").pack(anchor="w", padx=padx, pady=(6,0))
        # notes
        tk.Label(sf, text="Notes:", bg="#0b1220", fg="#cfe8ff", font=FONT_NAME).pack(anchor="w", padx=padx, pady=(8,0))
        self.notes_text = tk.Text(sf, height=8, width=80, font=FONT_NAME)
        self.notes_text.pack(padx=padx, pady=6)
        if self.task and self.task["notes"]:
            self.notes_text.insert(tk.END, self.task["notes"])
        if self.readonly:
            self.notes_text.config(state="disabled")
        # attachments
        tk.Label(sf, text="Attachments:", bg="#0b1220", fg="#cfe8ff", font=FONT_NAME).pack(anchor="w", padx=padx, pady=(6,0))
        att_frame = tk.Frame(sf, bg="#0b1220")
        att_frame.pack(padx=padx, pady=6, fill="x")
        self.att_listbox = tk.Listbox(att_frame, height=6, width=60)
        self.att_listbox.pack(side="left", fill="both", expand=True)
        att_btns = tk.Frame(att_frame, bg="#0b1220")
        att_btns.pack(side="left", padx=8)
        self.browse_btn = tk.Button(att_btns, text="Browse", width=14, command=self.browse_attachment)
        self.browse_btn.pack(pady=(0,6))
        self.open_btn = tk.Button(att_btns, text="Open/Preview", width=14, command=self.open_attachment)
        self.open_btn.pack(pady=(0,6))
        self.del_att_btn = tk.Button(att_btns, text="Delete Attachment", width=14, command=self.delete_selected_attachment)
        self.del_att_btn.pack()
        if self.readonly:
            self.browse_btn.config(state="disabled"); self.open_btn.config(state="normal"); self.del_att_btn.config(state="disabled")
        # links
        tk.Label(sf, text="Reference Links (name & URL):", bg="#0b1220", fg="#cfe8ff", font=FONT_NAME).pack(anchor="w", padx=padx, pady=(8,0))
        link_frame = tk.Frame(sf, bg="#0b1220")
        link_frame.pack(padx=padx, pady=6, fill="x")
        self.link_name_var = tk.StringVar()
        self.link_url_var = tk.StringVar()
        tk.Entry(link_frame, textvariable=self.link_name_var, width=20, font=FONT_NAME).pack(side="left", padx=(0,6))
        tk.Entry(link_frame, textvariable=self.link_url_var, width=52, font=FONT_NAME).pack(side="left", padx=(0,6))
        self.add_link_btn = tk.Button(link_frame, text="Add Link", command=self.add_link)
        self.add_link_btn.pack(side="left")
        if self.readonly:
            self.add_link_btn.config(state="disabled")
        self.link_listbox = tk.Listbox(sf, height=6, width=90)
        self.link_listbox.pack(padx=padx, pady=(6,0), fill="x")
        link_control_frame = tk.Frame(sf, bg="#0b1220")
        link_control_frame.pack(padx=padx, pady=(6,0), anchor="e")
        self.open_link_btn = tk.Button(link_control_frame, text="Open Link", command=self.open_selected_link)
        self.open_link_btn.pack(side="left", padx=6)
        self.del_link_btn = tk.Button(link_control_frame, text="Delete Link", command=self.delete_selected_link)
        self.del_link_btn.pack(side="left", padx=6)
        if self.readonly:
            self.open_link_btn.config(state="normal"); self.del_link_btn.config(state="disabled")
        # buttons
        btn_frame = tk.Frame(sf, bg="#0b1220")
        btn_frame.pack(pady=12)
        if not self.readonly:
            tk.Button(btn_frame, text="Save Task", width=14, command=self.save_task).pack(side="left", padx=6)
            tk.Button(btn_frame, text="Complete (feedback)", width=18, command=self.open_feedback_popup).pack(side="left", padx=6)
            tk.Button(btn_frame, text="Terminate (move to completed)", width=18, command=self.terminate_with_confirm).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Close", width=12, command=self._on_close).pack(side="left", padx=6)

    # attachments
    def browse_attachment(self):
        p = filedialog.askopenfilename(filetypes=[("Allowed files", "*.png *.jpg *.jpeg *.gif *.pdf *.ppt *.pptx *.doc *.docx *.xls *.xlsx *.mp3"), ("All files", "*.*")])
        if p:
            self.attachments_local.append(p)
            self.att_listbox.insert(tk.END, os.path.basename(p))

    def open_attachment(self):
        sel = self.att_listbox.curselection()
        if not sel:
            messagebox.showinfo("Open", "Select attachment first.")
            return
        i = sel[0]
        try:
            path = self.attachments_local[i]
        except IndexError:
            messagebox.showerror("Error", "Attachment path missing.")
            return
        if not os.path.exists(path):
            messagebox.showerror("Error", "File not found.")
            return
        ext = os.path.splitext(path)[1].lower()
        if ext in (".png", ".jpg", ".jpeg", ".gif"):
            try:
                top = tk.Toplevel(self)
                top.title(os.path.basename(path))
                img = Image.open(path)
                img.thumbnail((1000, 800))
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(top, image=photo)
                lbl.image = photo
                lbl.pack()
            except Exception:
                safe_open(path)
        else:
            safe_open(path)

    def delete_selected_attachment(self):
        sel = self.att_listbox.curselection()
        if not sel:
            messagebox.showinfo("Delete", "Select attachment to delete.")
            return
        idx = sel[0]
        db_count = len(self.db_attachments)
        if idx < db_count:
            att = self.db_attachments[idx]
            if messagebox.askyesno("Delete", f"Delete attachment '{att['file_name']}'? This will remove the file."):
                try:
                    delete_attachment_db(att["id"])
                except:
                    pass
                del self.db_attachments[idx]
                try:
                    self.attachments_local.remove(att["file_path"])
                except:
                    pass
                self.att_listbox.delete(idx)
        else:
            real = idx
            if messagebox.askyesno("Remove", "Remove unsaved attachment?"):
                try:
                    del self.attachments_local[real]
                except:
                    pass
                self.att_listbox.delete(idx)

    # links
    def add_link(self):
        n = self.link_name_var.get().strip()
        u = self.link_url_var.get().strip()
        if not n or not u:
            messagebox.showerror("Error", "Both name and URL required.")
            return
        self.links_new.append((n, u))
        self.link_listbox.insert(tk.END, f"{n} | {u}")
        self.link_name_var.set(""); self.link_url_var.set("")

    def open_selected_link(self):
        sel = self.link_listbox.curselection()
        if not sel:
            messagebox.showinfo("Open", "Select a link first.")
            return
        i = sel[0]
        if i < len(self.links_db):
            url = self.links_db[i]["url"]
        else:
            url = self.links_new[i - len(self.links_db)][1]
        try:
            webbrowser.open(url)
        except:
            messagebox.showerror("Error", "Cannot open link.")

    def delete_selected_link(self):
        sel = self.link_listbox.curselection()
        if not sel:
            messagebox.showinfo("Delete", "Select a link first.")
            return
        i = sel[0]
        if i < len(self.links_db):
            linkrow = self.links_db[i]
            if messagebox.askyesno("Delete", f"Delete saved link '{linkrow['name']}'?"):
                try:
                    delete_task_link_db(linkrow["id"])
                except:
                    pass
                del self.links_db[i]
                self.link_listbox.delete(i)
        else:
            real = i - len(self.links_db)
            if messagebox.askyesno("Delete", "Remove unsaved link?"):
                del self.links_new[real]
                self.link_listbox.delete(i)

    # save
    def save_task(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Task name required.")
            return
        folder_name = self.folder_var.get()
        folder_id = None
        for fid, fname in self.folder_map:
            if fname == folder_name:
                folder_id = fid; break
        date_str = self.cal.get_date()
        time_str = f"{self.hour_var.get()}:{self.min_var.get()} {self.ampm_var.get()}"
        notes = self.notes_text.get("1.0", tk.END).strip()
        repeat_daily = 1 if self.repeat_var.get() else 0

        if self.task:
            task_id = self.task["id"]
            update_task(task_id, name, date_str, time_str, notes, folder_id, repeat_daily)
        else:
            task_id = add_task(name, date_str, time_str, notes, folder_id, repeat_daily)
            # set self.task to new row for further operations
            self.task = fetch_task_by_id(task_id)

        # attachments: attachments_local may include DB paths and new paths
        existing_rows = fetch_attachments(task_id)
        existing_names = [r["file_name"] for r in existing_rows]
        for p in list(self.attachments_local):
            fname = os.path.basename(p)
            if fname in existing_names:
                continue
            if os.path.abspath(ATTACHMENT_DIR) in os.path.abspath(p):
                # insert DB record pointing to existing file
                conn = get_conn()
                conn.execute("INSERT INTO attachments(task_id,file_name,file_path) VALUES(?,?,?)", (task_id, fname, os.path.abspath(p)))
                conn.commit(); conn.close()
            else:
                try:
                    save_attachment_db(task_id, p)
                except:
                    conn = get_conn()
                    conn.execute("INSERT INTO attachments(task_id,file_name,file_path) VALUES(?,?,?)", (task_id, fname, p))
                    conn.commit(); conn.close()

        # links
        for (n,u) in self.links_new:
            save_task_link_db(task_id, n, u)

        self.master.refresh_tasks()
        messagebox.showinfo("Saved", "Task saved.")
        # reload internal DB attachment lists
        self.db_attachments = fetch_attachments(task_id)
        self.attachments_local = [r["file_path"] for r in self.db_attachments]
        # ensure listbox reflects DB state
        self.att_listbox.delete(0, tk.END)
        for r in self.db_attachments:
            self.att_listbox.insert(tk.END, r["file_name"])

    # feedback popup (used in modal)
    def open_feedback_popup(self):
        popup = tk.Toplevel(self)
        popup.transient(self)
        popup.grab_set()
        popup.title("Feedback")
        popup.configure(bg="#071428")
        tk.Label(popup, text="Choose feedback:", bg="#071428", fg="#cfe8ff", font=(FONT_NAME[0], int(12*FONT_SCALE), "bold")).pack(pady=10, padx=10)
        chosen = tk.StringVar(value="Perfect")
        def choose_and_close():
            val = chosen.get()
            comment = None
            if val == "Other":
                comment = comment_box.get("1.0", tk.END).strip()
            task_id = self.task["id"] if self.task else None
            if not task_id:
                if messagebox.askyesno("Save then complete", "Task must be saved before completing. Save now?"):
                    self.save_task()
                    task_id = self.task["id"] if self.task else None
                else:
                    popup.destroy(); return
            if task_id:
                complete_task_with_feedback(task_id, val, comment)
                self.master.refresh_tasks()
                messagebox.showinfo("Completed", "Task marked complete with feedback.")
            popup.destroy()
            self._on_close()
        frame = tk.Frame(popup, bg="#071428")
        frame.pack(pady=6)
        options = ["Perfect", "Good", "Average", "Poor", "Other"]
        for o in options:
            tk.Radiobutton(frame, text=o, variable=chosen, value=o, indicatoron=0, width=12, padx=6, bg="#0b3a54", fg="white").pack(side="left", padx=4, pady=6)
        comment_box = tk.Text(popup, height=4, width=60)
        tk.Label(popup, text="Comment (only for Other):", bg="#071428", fg="#cfe8ff").pack(pady=(8,0))
        comment_box.pack(padx=8, pady=6)
        tk.Button(popup, text="Save Feedback & Complete", command=choose_and_close).pack(pady=8)

    def terminate_with_confirm(self):
        if not self.task:
            if messagebox.askyesno("Save & Terminate", "Task must be saved first. Save now?"):
                self.save_task()
            else:
                return
        tid = self.task["id"] if self.task else None
        if not tid:
            conn = get_conn(); row = conn.execute("SELECT id FROM tasks ORDER BY id DESC LIMIT 1").fetchone(); conn.close()
            tid = row["id"] if row else None
        if not tid:
            messagebox.showerror("Error", "Cannot determine task id.")
            return
        if messagebox.askyesno("Terminate", "Terminate this task (mark as completed/terminated)?"):
            complete_task_with_feedback(tid, "Terminated", comment=None, terminated=True)
            self.master.refresh_tasks()
            messagebox.showinfo("Terminated", "Task terminated and moved to completed.")
            self._on_close()

    def _on_close(self):
        self._unbind_mousewheel()
        try:
            self.grab_release()
        except:
            pass
        # unset modal flag reliably
        try:
            self.master.modal_open = False
        except:
            pass
        self.destroy()

# -------------------------
# Main App window
# -------------------------
class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        try:
            self.state("zoomed")
        except:
            self.geometry("1200x780")
        self.configure(bg="#071428")
        self.modal_open = False
        self.current_folder_id = None
        self._build_ui()
        self._start_midnight_watcher()
        self.refresh_folders()
        folders = fetch_folders()
        if folders:
            self.select_folder(folders[0]["id"])

    def _build_ui(self):
        left = tk.Frame(self, bg="#071428", width=320)
        left.grid(row=0, column=0, sticky="nsw", padx=(8,8), pady=8)
        left.grid_propagate(False)
        tk.Label(left, text="Folders", font=(FONT_NAME[0], int(12*FONT_SCALE), "bold"), bg="#071428", fg="#cfe8ff").pack(anchor="nw", padx=8, pady=(6,6))
        self.folder_listbox = tk.Listbox(left, bg="#0b1220", fg="white", width=30, activestyle="dotbox", font=FONT_NAME, selectbackground="#004b7a")
        self.folder_listbox.pack(fill="both", expand=True, padx=8)
        self.folder_listbox.bind("<<ListboxSelect>>", lambda e: self.on_folder_select())
        folder_btns = tk.Frame(left, bg="#071428")
        folder_btns.pack(pady=8)
        tk.Button(folder_btns, text="+ New Folder", command=self.add_folder_ui, width=12).pack(side="left", padx=4)
        tk.Button(folder_btns, text="✏ Rename", command=self.rename_folder_ui, width=10).pack(side="left", padx=4)
        tk.Button(folder_btns, text="🗑 Delete", command=self.delete_folder_ui, width=10).pack(side="left", padx=4)
        bottom_opts = tk.Frame(left, bg="#071428")
        bottom_opts.pack(pady=10, fill="x")
        tk.Button(bottom_opts, text="Daily Habit", command=lambda: self.select_special("Daily Habit"), width=12).pack(side="left", padx=4)
        tk.Button(bottom_opts, text="Health Care", command=lambda: self.select_special("Health Care"), width=12).pack(side="left", padx=4)
        tk.Button(bottom_opts, text="Time Reference", command=lambda: self.select_special("Time Reference"), width=12).pack(side="left", padx=4)

        right = tk.Frame(self, bg="#071428")
        right.grid(row=0, column=1, sticky="nsew", padx=(8,12), pady=8)
        right.grid_rowconfigure(1, weight=3)
        right.grid_rowconfigure(2, weight=2)
        right.grid_columnconfigure(0, weight=1)
        top = tk.Frame(right, bg="#071428")
        top.grid(row=0, column=0, sticky="ew", pady=(0,8))
        tk.Label(top, text="Search Pending:", bg="#071428", fg="#cfe8ff", font=FONT_NAME).pack(side="left", padx=(6,6))
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(top, textvariable=self.search_var, width=44, font=FONT_NAME)
        self.search_entry.pack(side="left", padx=(0,12))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_tasks())
        btn_frame = tk.Frame(top, bg="#071428")
        btn_frame.pack(side="right", padx=6)
        ttk.Button(btn_frame, text="+ Add Task", command=self.add_task_ui).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="✏ Edit Task", command=self.edit_task_ui).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="🗑 Delete Task", command=self.delete_task_ui).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="✔ Complete Task", command=self.complete_task_ui).pack(side="left", padx=6)

        tree_frame = tk.Frame(right, bg="#071428")
        tree_frame.grid(row=1, column=0, sticky="nsew")
        cols = ("ID","Name","Due Date","Due Time","Folder")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="w", width=220 if c=="Name" else 120)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", lambda e: self.open_task_detail())

        tk.Label(right, text="Completed Tasks", bg="#071428", fg="#cfe8ff", font=(FONT_NAME[0], int(12*FONT_SCALE), "bold")).grid(row=2, column=0, sticky="w", pady=(12,0))
        done_frame = tk.Frame(right, bg="#071428")
        done_frame.grid(row=2, column=0, sticky="nsew", pady=(36,0))
        self.tree_done = ttk.Treeview(done_frame, columns=("ID","Name","Completed At","Feedback","Folder"), show="headings", height=8)
        for c in ("ID","Name","Completed At","Feedback","Folder"):
            self.tree_done.heading(c, text=c)
            self.tree_done.column(c, anchor="w", width=220 if c=="Name" else 140)
        self.tree_done.pack(fill="both", expand=True)
        self.tree_done.bind("<Double-1>", lambda e: self.open_task_detail_done())

    # folders
    def refresh_folders(self):
        self.folder_listbox.delete(0, tk.END)
        self._folders = fetch_folders()
        for f in self._folders:
            self.folder_listbox.insert(tk.END, f["name"])

    def on_folder_select(self):
        sel = self.folder_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        fid = self._folders[idx]["id"]
        self.select_folder(fid)

    def select_folder(self, fid):
        self.current_folder_id = fid
        for i, f in enumerate(self._folders):
            if f["id"] == fid:
                self.folder_listbox.selection_clear(0, tk.END)
                self.folder_listbox.selection_set(i)
                self.folder_listbox.see(i)
                break
        self.refresh_tasks()

    def select_special(self, name):
        for f in self._folders:
            if f["name"] == name:
                self.select_folder(f["id"])
                return

    def add_folder_ui(self):
        n = simpledialog.askstring("New Folder", "Folder name:", parent=self)
        if not n:
            return
        try:
            add_folder(n)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot add folder: {e}")
            return
        self.refresh_folders()

    def rename_folder_ui(self):
        sel = self.folder_listbox.curselection()
        if not sel:
            messagebox.showinfo("Rename", "Select a folder first.")
            return
        idx = sel[0]; fid = self._folders[idx]["id"]; current = self._folders[idx]["name"]
        new = simpledialog.askstring("Rename Folder", "New name:", initialvalue=current, parent=self)
        if new and new.strip():
            rename_folder(fid, new.strip())
            self.refresh_folders()

    def delete_folder_ui(self):
        sel = self.folder_listbox.curselection()
        if not sel:
            messagebox.showinfo("Delete", "Select a folder first.")
            return
        idx = sel[0]; fid = self._folders[idx]["id"]; name = self._folders[idx]["name"]
        if messagebox.askyesno("Delete", f"Delete folder '{name}' and all tasks?"):
            try:
                delete_folder(fid)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot delete: {e}")
            self.refresh_folders()
            folders = fetch_folders()
            if folders:
                self.select_folder(folders[0]["id"])
            else:
                self.current_folder_id = None
            self.refresh_tasks()

    # refresh tasks
    def refresh_tasks(self):
        st = self.search_var.get().lower()
        for r in self.tree.get_children():
            self.tree.delete(r)
        try:
            rows = fetch_tasks(0, folder_id=self.current_folder_id)
        except:
            rows = []
        for t in rows:
            if st and st not in t["name"].lower():
                continue
            folder_name = ""
            if t["folder_id"]:
                for f in self._folders:
                    if f["id"] == t["folder_id"]:
                        folder_name = f["name"]; break
            # color highlight for overdue/uncompleted may be added later; treeview cell color is limited
            self.tree.insert("", "end", values=(t["id"], t["name"], t["due_date"], t["due_time"], folder_name))
        for r in self.tree_done.get_children():
            self.tree_done.delete(r)
        rows_done = fetch_tasks(1, folder_id=self.current_folder_id)
        for t in rows_done:
            folder_name = ""
            if t["folder_id"]:
                for f in self._folders:
                    if f["id"] == t["folder_id"]:
                        folder_name = f["name"]; break
            self.tree_done.insert("", "end", values=(t["id"], t["name"], t["completed_at"] or "", t["feedback"] or "", folder_name))

    # actions
    def add_task_ui(self):
        if self.modal_open:
            return
        self.modal_open = True
        default = self.current_folder_id
        m = TaskModal(self, "Add Task", task=None, readonly=False, default_folder_id=default)
        # set callback to reset flag when modal destroyed
        m.wait_window()
        self.modal_open = False
        self.refresh_tasks()

    def edit_task_ui(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Edit", "Select a task first.")
            return
        tid = self.tree.item(sel[0])["values"][0]
        task = fetch_task_by_id(tid)
        if not task:
            messagebox.showerror("Error", "Task not found.")
            return
        if self.modal_open:
            return
        self.modal_open = True
        m = TaskModal(self, "Edit Task", task=task, readonly=False, default_folder_id=task["folder_id"])
        m.wait_window()
        self.modal_open = False
        self.refresh_tasks()

    def delete_task_ui(self):
        sel = self.tree.selection()
        if sel:
            tid = self.tree.item(sel[0])["values"][0]
            if messagebox.askyesno("Delete", "Delete selected task?"):
                delete_task(tid)
        sel2 = self.tree_done.selection()
        if sel2:
            tid = self.tree_done.item(sel2[0])["values"][0]
            if messagebox.askyesno("Delete", "Delete selected completed task?"):
                delete_task(tid)
        self.refresh_tasks()

    def complete_task_ui(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Complete", "Select a task to complete.")
            return
        tid = self.tree.item(sel[0])["values"][0]
        popup = tk.Toplevel(self)
        popup.transient(self)
        popup.grab_set()
        popup.title("Feedback")
        tk.Label(popup, text="Feedback (choose):").pack(pady=6)
        choice = tk.StringVar(value="Perfect")
        for o in ["Perfect","Good","Average","Poor","Other"]:
            tk.Radiobutton(popup, text=o, variable=choice, value=o).pack(side="left", padx=6, pady=6)
        comment = tk.Text(popup, height=4, width=60)
        tk.Label(popup, text="Comment (for Other):").pack()
        comment.pack()
        def do_complete():
            val = choice.get()
            c = comment.get("1.0", tk.END).strip() if val=="Other" else ""
            complete_task_with_feedback(tid, val, c)
            popup.destroy()
            self.refresh_tasks()
        tk.Button(popup, text="Save & Complete", command=do_complete).pack(pady=6)

    def open_task_detail(self):
        sel = self.tree.selection()
        if not sel: return
        tid = self.tree.item(sel[0])["values"][0]
        task = fetch_task_by_id(tid)
        if not task: return
        if self.modal_open: return
        self.modal_open = True
        m = TaskModal(self, "Task Details", task=task, readonly=True)
        m.wait_window()
        self.modal_open = False
        self.refresh_tasks()

    def open_task_detail_done(self):
        sel = self.tree_done.selection()
        if not sel: return
        tid = self.tree_done.item(sel[0])["values"][0]
        task = fetch_task_by_id(tid)
        if not task: return
        if self.modal_open: return
        self.modal_open = True
        m = TaskModal(self, "Completed Task Details", task=task, readonly=True)
        m.wait_window()
        self.modal_open = False
        self.refresh_tasks()

    def open_time_reference(self):
        ex_names = ("Daily Habit","Health Care")
        exclude = [f["id"] for f in self._folders if f["name"] in ex_names]
        conn = get_conn()
        rows = conn.execute("SELECT * FROM tasks").fetchall()
        conn.close()
        filtered = [r for r in rows if r["folder_id"] not in exclude]
        filtered.sort(key=lambda x: x["id"], reverse=True)
        top = tk.Toplevel(self)
        top.title("Time Reference")
        top.geometry("1000x700")
        top.configure(bg="#071428")
        canvas = tk.Canvas(top, bg="#071428")
        vs = ttk.Scrollbar(top, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg="#071428")
        canvas.create_window((0,0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=vs.set)
        canvas.pack(side="left", fill="both", expand=True)
        vs.pack(side="right", fill="y")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        for t in filtered:
            frame = tk.Frame(inner, bg="#0b1220", bd=1, relief="raised")
            frame.pack(fill="x", padx=8, pady=6)
            bgc = "#0b1220"
            if t["terminated"]:
                bgc = "#6a0000"
            elif t["completed"]:
                fb = (t["feedback"] or "").lower()
                if fb in ("perfect","good"):
                    bgc = "#006400"
                elif fb in ("average","poor"):
                    bgc = "#b8860b"
                elif fb == "other":
                    bgc = "#20b2aa"
                else:
                    bgc = "#073642"
            else:
                if t["due_date"]:
                    try:
                        d = date.fromisoformat(t["due_date"])
                        if d < date.today():
                            bgc = "#5a0000"  # red-ish for overdue
                    except:
                        pass
            frame.configure(bg=bgc)
            fname = ""
            for f in self._folders:
                if f["id"] == t["folder_id"]:
                    fname = f["name"]; break
            txt = f"ID {t['id']} | {t['name']} | {t['due_date']} {t['due_time']} | Folder: {fname}"
            tk.Label(frame, text=txt, bg=bgc, fg="white", font=FONT_NAME).pack(anchor="w", padx=8, pady=6)
            btnf = tk.Frame(frame, bg=bgc)
            btnf.pack(anchor="e", padx=8, pady=(0,6))
            def _open_task(tt=t):
                # open in modal view (readonly)
                if self.modal_open:
                    return
                self.modal_open = True
                m = TaskModal(self, "View Task", task=tt, readonly=True)
                m.wait_window()
                self.modal_open = False
            tk.Button(btnf, text="View", command=_open_task).pack(side="left", padx=6)

    # midnight watcher: check every 30 seconds
    def _start_midnight_watcher(self):
        self._last_checked_date = date.today()
        def check():
            try:
                now = datetime.now()
                today = now.date()
                if today != self._last_checked_date:
                    self._last_checked_date = today
                    duplicate_daily_tasks_for_date(today)
            except Exception as e:
                print("Watcher error:", e)
            # schedule next check
            self.after(30000, check)
        # start first check
        self.after(30000, check)

if __name__ == "__main__":
    init_db()
    app = TodoApp()
    app.mainloop()
