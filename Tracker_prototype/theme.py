# File: theme.py
"""
Modern, flat‑styled theme for your Tkinter/ttk app.
No extra libraries required.
"""

import tkinter as tk
from tkinter import ttk

def apply_base_theme(root: tk.Tk | ttk.Frame) -> None:
    # ──────────────────────────────────────────────────────────
    # 1. Use a more modern base ttk theme
    #    'clam' ships with Tk and is cleaner than 'default' / 'classic'.
    #    You can switch to 'alt', 'vista', or others if you prefer.
    # ──────────────────────────────────────────────────────────
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        # Fallback if 'clam' isn't available (rare)
        style.theme_use(style.theme_names()[0])

    # ──────────────────────────────────────────────────────────
    # 2. Core design tokens (update here for quick re‑skinning)
    # ──────────────────────────────────────────────────────────
    COLORS = {
        "base_bg"   : "#f4f6f8",   # very light gray
        "surface"   : "#ffffff",   # cards / entries
        "button_bg" : "#e1e7ef",   # light button
        "button_hover": "#000000", # accent when hovering / active
        "text"      : "#1d1d1f",   # almost‑black text
        "subtext"   : "#555",
        "accent"    : "#000000",   # primary brand color
        "border"    : "#d0d5db",   # subtle borders
    }

    FONT = ("Segoe UI", 10)

    # Apply app‑wide defaults
    root.configure(bg=COLORS["base_bg"])
    root.option_add("*Font", FONT)
    root.option_add("*Entry.Font", FONT)
    root.option_add("*Text.Font", FONT)

    # ──────────────────────────────────────────────────────────
    # 3. ✨ Widget styles
    # ──────────────────────────────────────────────────────────
    # -- Labels ------------------------------------------------
    style.configure(
        "TLabel",
        background=COLORS["base_bg"],
        foreground=COLORS["text"],
        padding=2,
    )

    # -- Buttons ----------------------------------------------
    style.configure(
        "TButton",
        background=COLORS["button_bg"],
        foreground=COLORS["text"],
        borderwidth=0,
        padding=(10, 6),
        relief="flat",
        font=FONT,
    )
    style.map(
        "TButton",
        background=[
            ("active", COLORS["button_hover"]),
            ("pressed", COLORS["button_hover"]),
            ("disabled", COLORS["button_bg"]),
        ],
        foreground=[
            ("active", "white"),
            ("pressed", "white"),
            ("disabled", COLORS["subtext"]),
        ],
    )

    # -- Checkbuttons -----------------------------------------
    style.configure(
        "TCheckbutton",
        background=COLORS["base_bg"],
        foreground=COLORS["text"],
        padding=4,
    )

    # -- Entries ----------------------------------------------
    style.configure(
        "TEntry",
        fieldbackground=COLORS["surface"],
        foreground=COLORS["text"],
        padding=8,
        bordercolor=COLORS["border"],
        borderwidth=1,
        relief="flat",
    )
    style.map(
        "TEntry",
        bordercolor=[("focus", COLORS["accent"])],
        fieldbackground=[("disabled", COLORS["base_bg"])]
    )

    # -- Text widget (inside custom frames) -------------------
    # You embed Text widgets yourself, so we’ll just set system
    # colors so they look integrated.
    root.option_add("*Text.background", COLORS["surface"])
    root.option_add("*Text.foreground", COLORS["text"])
    root.option_add("*Text.borderwidth", 0)
    root.option_add("*Text.highlightthickness", 1)
    root.option_add("*Text.highlightcolor", COLORS["accent"])
    root.option_add("*Text.highlightbackground", COLORS["border"])

    # -- Scrollbars -------------------------------------------
    style.configure(
        "Vertical.TScrollbar",
        background=COLORS["button_bg"],
        troughcolor=COLORS["base_bg"],
        borderwidth=0,
        arrowcolor=COLORS["text"],
    )
    style.configure(
        "Horizontal.TScrollbar",
        background=COLORS["button_bg"],
        troughcolor=COLORS["base_bg"],
        borderwidth=0,
        arrowcolor=COLORS["text"],
    )

    # ──────────────────────────────────────────────────────────
    # 4. Make headings / frames inherit the background
    #    so large blank areas match the new base_bg.
    # ──────────────────────────────────────────────────────────
    style.configure("TFrame", background=COLORS["base_bg"])
    style.configure("TLabelframe", background=COLORS["base_bg"])

    # ──────────────────────────────────────────────────────────
    # 5. Done! Re‑draw
    # ──────────────────────────────────────────────────────────
    root.update_idletasks()
