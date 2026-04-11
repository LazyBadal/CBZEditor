import tkinter as tk
from tkinter import filedialog
import threading
from core import process_folder

# ---------- colors ----------
BG = "#0f0f0f"
FG = "#ffffff"
SUBTLE = "#888888"
ENTRY_BG = "#1a1a1a"
BTN_BG = "#1f1f1f"
ACCENT = "#3a86ff"
TITLE_BG = "#1c1c1c"

# ---------- window ----------
root = tk.Tk()
root.overrideredirect(True)
root.geometry("420x380")
root.configure(bg=BG)

# ---------- drag ----------
def start_move(e):
    root.x = e.x
    root.y = e.y

def move(e):
    root.geometry(f"+{e.x_root - root.x}+{e.y_root - root.y}")

# ---------- title bar ----------
bar = tk.Frame(root, bg=TITLE_BG, height=28)
bar.pack(fill="x")

tk.Label(bar, text="cbz-tool", bg=TITLE_BG, fg=FG).pack(side="left", padx=10)

close_btn = tk.Label(bar, text="✕", bg=TITLE_BG, fg=FG)
close_btn.pack(side="right", padx=10)
close_btn.bind("<Button-1>", lambda e: root.destroy())

bar.bind("<Button-1>", start_move)
bar.bind("<B1-Motion>", move)

# ---------- vars ----------
mode_var = tk.StringVar(value="manual")

folder_var = tk.StringVar()
db_var = tk.StringVar()

series_var = tk.StringVar()
author_var = tk.StringVar()
tags_var = tk.StringVar()
summary_var = tk.StringVar()

status_var = tk.StringVar()

# ---------- helpers ----------
def browse_folder():
    folder_var.set(filedialog.askdirectory())

def browse_db():
    db_var.set(filedialog.askopenfilename(filetypes=[("DB", "*.db")]))

def field(label, var, y):
    lbl = tk.Label(root, text=label, bg=BG, fg=SUBTLE)
    entry = tk.Entry(root, textvariable=var,
                     bg=ENTRY_BG, fg=FG,
                     insertbackground=FG,
                     relief="flat")
    return lbl, entry

# ---------- run ----------
def run():
    def task():
        try:
            if mode_var.get() == "db":
                count = process_folder(
                    folder_var.get(),
                    db_var.get(),
                    "", "", "", ""
                )
            else:
                count = process_folder(
                    folder_var.get(),
                    "",  # no DB
                    series_var.get(),
                    author_var.get(),
                    tags_var.get(),
                    summary_var.get()
                )

            status_var.set(f"Done ✔ ({count} files)")
        except Exception as e:
            status_var.set(f"Error: {e}")

    status_var.set("Processing...")
    threading.Thread(target=task, daemon=True).start()

# ---------- widgets ----------

# Mode
mode_manual = tk.Radiobutton(root, text="Manual",
                             variable=mode_var, value="manual",
                             command=lambda: update_mode(),
                             bg=BG, fg=FG, selectcolor=BG)

mode_db = tk.Radiobutton(root, text="Calibre DB",
                         variable=mode_var, value="db",
                         command=lambda: update_mode(),
                         bg=BG, fg=FG, selectcolor=BG)

# Folder
folder_label, folder_entry = field("Folder", folder_var, 70)
folder_btn = tk.Button(root, text="...", command=browse_folder, bg=BTN_BG, fg=FG)

# DB
db_label, db_entry = field("Calibre DB", db_var, 110)
db_btn = tk.Button(root, text="...", command=browse_db, bg=BTN_BG, fg=FG)

# Manual fields
series_label, series_entry = field("Series", series_var, 110)
author_label, author_entry = field("Author", author_var, 150)
tags_label, tags_entry = field("Tags", tags_var, 190)
summary_label, summary_entry = field("Summary", summary_var, 230)

# Run + status
run_btn = tk.Button(root, text="Run", command=run, bg=BTN_BG, fg=FG)
status_label = tk.Label(root, textvariable=status_var, bg=BG, fg="#00ff88")

# ---------- base layout ----------
mode_manual.place(x=12, y=35)
mode_db.place(x=120, y=35)

folder_label.place(x=12, y=70)
folder_entry.place(x=12, y=90, width=368)
folder_btn.place(x=385, y=90, width=23)

# ---------- mode switch ----------
def update_mode():
    if mode_var.get() == "db":
        # show DB
        db_label.place(x=12, y=110)
        db_entry.place(x=12, y=130, width=368)
        db_btn.place(x=385, y=130, width=23)

        # hide manual
        series_label.place_forget()
        series_entry.place_forget()
        author_label.place_forget()
        author_entry.place_forget()
        tags_label.place_forget()
        tags_entry.place_forget()
        summary_label.place_forget()
        summary_entry.place_forget()

    else:
        # hide DB
        db_label.place_forget()
        db_entry.place_forget()
        db_btn.place_forget()

        # show manual
        series_label.place(x=12, y=110)
        series_entry.place(x=12, y=130, width=368)

        author_label.place(x=12, y=150)
        author_entry.place(x=12, y=170, width=368)

        tags_label.place(x=12, y=190)
        tags_entry.place(x=12, y=210, width=368)

        summary_label.place(x=12, y=230)
        summary_entry.place(x=12, y=250, width=368)

# Run + status
run_btn.place(x=12, y=300, width=368)
status_label.place(x=12, y=340)

# init
update_mode()
root.mainloop()