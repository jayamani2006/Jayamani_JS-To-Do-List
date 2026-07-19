import tkinter as tk
from PIL import Image, ImageTk
import subprocess, os
import sys

BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# ===================== JS TO-DO-LIST – NEON GLOW WELCOME PANEL =====================

guide_text = """
Welcome to the advanced To-Do-List!

🚀 JS To-Do List App – Futuristic Edition

Supported:
• Links
• MP3
• DOCX
• XLSX
• Images
• PDFs
• Any file attachment

Quick Start:
1. Launch JS To-Do List.exe
2. Add tasks with attachments
3. Auto-save always enabled
4. Attachments stored in task_attachments folder

Tips:
• Short titles help faster searching
• Attachments remain even after editing

Stay productive. Stay futuristic. ⚡
"""

# Window
root = tk.Tk()
root.title("Welcome – JS To-Do List")
root.geometry("520x600")
root.configure(bg="#020611")
root.resizable(False, False)

# Neon border around window
border = tk.Frame(root, bg="#00eaff", height=3)
border.pack(fill="x")

# Logo
try:
    logo_path = os.path.join(BASE_DIR, '..', 'assets', 'icons', 'icon.ico')
    img = Image.open(logo_path)
    img = img.resize((110, 110), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(img)
    tk.Label(root, image=logo, bg="#020611").pack(pady=20)
except:
    tk.Label(root, text="[Logo Missing]", fg="#00eaff", bg="#020611").pack(pady=20)

# Title
tk.Label(
    root,
    text="JS To-Do-List",
    font=("Segoe UI", 30, "bold"),
    fg="#00eaff",
    bg="#020611"
).pack()

# Developer text
tk.Label(
    root,
    text="DEVELOPED BY Chip-X\n  Jayasubramani",
    font=("Segoe UI", 12),
    fg="#6cdcff",
    bg="#020611"
).pack(pady=10)

# Text panel with glow effect
frame_text = tk.Frame(root, bg="#02101f", bd=2, relief="ridge", highlightthickness=2)
frame_text.config(highlightbackground="#00eaff", highlightcolor="#00eaff")
frame_text.pack(pady=20, padx=25, fill="both", expand=True)

text_widget = tk.Text(
    frame_text,
    wrap="word",
    font=("Segoe UI", 13),
    bg="#02101f",
    fg="#e8faff",
    bd=0
)
text_widget.insert("1.0", guide_text)
text_widget.config(state="disabled")
text_widget.pack(expand=True, fill="both", padx=10, pady=10)

# Launch function
def open_app():
    exe_path = os.path.join(BASE_DIR, '..', 'JS-To-Do-List.exe')
    if os.path.exists(exe_path):
        subprocess.Popen([exe_path])
    root.destroy()

# Button glow effects
def glow_in(e):
    start_btn.config(bg="#00ffff", fg="#00121f")

def glow_out(e):
    start_btn.config(bg="#00eaff", fg="#00121f")

# Button Frame
frame_btn = tk.Frame(root, bg="#020611")
frame_btn.pack(pady=15)

# Glowing start button
start_btn = tk.Button(
    frame_btn,
    text="Open App",
    command=open_app,
    font=("Segoe UI", 17, "bold"),
    bg="#00eaff",
    fg="#00121f",
    activebackground="#00ffff",
    activeforeground="#00121f",
    bd=0,
    padx=22,
    pady=12
)
start_btn.pack()

start_btn.bind("<Enter>", glow_in)
start_btn.bind("<Leave>", glow_out)

root.mainloop()
