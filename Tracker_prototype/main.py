# File: main.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from layout import build_layout, add_control_buttons
from theme import apply_base_theme

# Create main themed window
root = ttk.Window(themename="darkly")  # Try "darkly", "morph", etc. for other looks
apply_base_theme(root)
root.title("DSA Revision Tracker — Dynamic Rows")
root.geometry("1650x750")

# === TOP TOOLBAR ===
topbar = ttk.Frame(root)
topbar.pack(side="top", fill="x", padx=10, pady=5)

# === Canvas for scrolling ===
canvas = ttk.Canvas(root, highlightthickness=0)
scroll_x = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
scroll_y = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# === Frame inside canvas ===
frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# === Build layout + controls ===
build_layout(frame)
add_control_buttons(topbar, frame)

# === Scroll binding ===
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

root.mainloop()
