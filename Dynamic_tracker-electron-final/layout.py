import tkinter as tk
from tkinter import ttk, messagebox
from constants import COLUMNS, DEFAULT_LINK, HEADER_BG
from storage import save_all_rows, load_all_rows
from logic import calculate_last_performance, estimate_next_review
import datetime

# Containers for each row's widgets
all_rows = []  # Each item: {'entries': {}, 'checkboxes': {}, 'notes': {}, 'labels': {}, 'widgets': []}
current_row_index = -1  # We'll track which is the last-added row

def build_layout(frame):
    for col_index, col_name in enumerate(COLUMNS):
        tk.Label(
            frame,
            text=col_name,
            relief="ridge",
            width=15,
            anchor='center',
            bg=HEADER_BG
        ).grid(row=0, column=col_index, sticky="nsew")
    add_new_row(frame)

def add_new_row(frame, data=None):
    global current_row_index
    row_index = len(all_rows) + 1
    current_row_index = row_index - 1

    entries, checkboxes, notes, labels, widgets = {}, {}, {}, {}, []

    def update_auto_labels():
        try:
            checkbox_state = {k: v.get() for k, v in checkboxes.items()}
            perf = calculate_last_performance(checkbox_state)
            labels["Last Performance"].config(text=perf)

            last_date = ""
            for try_key in ["4th Try (Date)", "3rd Try (Date)", "2nd Try (Date)", "1st Try (Date)"]:
                if entries.get(try_key) and entries[try_key].get():
                    last_date = entries[try_key].get()
                    break

            review = estimate_next_review(last_date, perf)
            labels["Next Review"].config(text=review)
        except Exception as e:
            print("Auto field error:", e)

    for col_index, col_name in enumerate(COLUMNS):
        grid_opts = {"row": row_index, "column": col_index, "sticky": "nsew", "padx": 2, "pady": 2}

        if col_name == "S.No":
            lbl = ttk.Label(frame, text=str(row_index), anchor='center')
            lbl.grid(**grid_opts)
            widgets.append(lbl)

        elif "Myself" in col_name or "Help" in col_name:
            var = tk.BooleanVar()
            checkboxes[col_name] = var
            cb = ttk.Checkbutton(frame, variable=var, command=update_auto_labels)
            cb.grid(**grid_opts)
            widgets.append(cb)

        elif "Notes" in col_name:
            container = tk.Frame(frame, background="white", highlightbackground="#ccc", highlightthickness=1)
            container.grid(**grid_opts)
            txt = tk.Text(container, height=2, width=20, relief="flat", bg="white", bd=0)
            txt.pack(fill="both", expand=True, padx=2, pady=2)
            notes[col_name] = txt
            widgets.append(container)

        elif "Last Performance" in col_name or "Next Review" in col_name:
            lbl = ttk.Label(frame, text="(auto)", anchor='center')
            lbl.grid(**grid_opts)
            labels[col_name] = lbl
            widgets.append(lbl)

        elif col_name == "Link":
            link_entry = ttk.Entry(frame, width=20)
            link_entry.insert(0, DEFAULT_LINK)
            link_entry.grid(**grid_opts)
            entries[col_name] = link_entry
            widgets.append(link_entry)

        else:
            entry = ttk.Entry(frame, width=20)
            entry.grid(**grid_opts)
            entries[col_name] = entry
            widgets.append(entry)
            if "Try (Date)" in col_name:
                entry.bind("<FocusOut>", lambda e: update_auto_labels())

    # Delete button
    def delete_this_row():
        for widget in widgets:
            widget.destroy()
        all_rows.remove(row_dict)

    delete_btn = ttk.Button(frame, text="🗑️", command=delete_this_row)
    delete_btn.grid(row=row_index, column=len(COLUMNS), sticky="nsew", padx=2, pady=2)
    widgets.append(delete_btn)

    if data:
        for k, v in data.items():
            if k in entries:
                entries[k].insert(0, v)
            elif k in checkboxes:
                checkboxes[k].set(v)
            elif k in notes:
                notes[k].insert("1.0", v)
        update_auto_labels()

    row_dict = {
        "entries": entries,
        "checkboxes": checkboxes,
        "notes": notes,
        "labels": labels,
        "widgets": widgets
    }

    frame.grid_rowconfigure(row_index, pad=2)  # Clean spacing
    all_rows.append(row_dict)


def check_today_alerts():
    today = datetime.date.today().strftime("%Y-%m-%d")
    due_items = []

    for index, row in enumerate(all_rows, 1):
        label = row["labels"].get("Next Review")
        if label:
            next_review = label.cget("text")
            if next_review == today:
                title_widget = row["entries"].get("Title")
                title = title_widget.get() if title_widget else "(No Title)"
                due_items.append(f"{index}. {title}")

    if due_items:
        messagebox.showinfo("📢 Today's Revisions", "You need to revise:\n\n" + "\n".join(due_items))
    else:
        print("✅ No revisions due today.")

def get_all_rows():
    return all_rows

def print_row_data():
    row = all_rows[-1] if all_rows else None
    if not row:
        print("No row available")
        return

    output = {}
    for k, v in row["entries"].items():
        output[k] = v.get()
    for k, v in row["checkboxes"].items():
        output[k] = v.get()
    for k, w in row["notes"].items():
        output[k] = w.get("1.0", tk.END).strip()

    print(f"\nRow {len(all_rows)} Data Snapshot:")
    print(output)
    return output

def save_all():
    data = []
    for row in all_rows:
        if all(v.get().strip() == "" for v in row["entries"].values()) and \
           all(not v.get() for v in row["checkboxes"].values()) and \
           all(w.get("1.0", tk.END).strip() == "" for w in row["notes"].values()):
            continue

        row_dict = {}
        for k, v in row["entries"].items():
            row_dict[k] = v.get()
        for k, v in row["checkboxes"].items():
            row_dict[k] = v.get()
        for k, w in row["notes"].items():
            row_dict[k] = w.get("1.0", tk.END).strip()
        data.append(row_dict)
    save_all_rows(data)

def load_all(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    all_rows.clear()

    build_layout(frame)
    data_list = load_all_rows()
    if not data_list:
        return

    for i, data in enumerate(data_list):
        if i == 0:
            add_new_row(frame, data)
        else:
            add_new_row(frame, data)

    check_today_alerts()  # 🔔 Show reminder alert after loading

def add_control_buttons(toolbar_frame, table_frame):
    ttk.Button(toolbar_frame, text="➕ Add Row", command=lambda: add_new_row(table_frame)).pack(side="left", padx=8)
    ttk.Button(toolbar_frame, text="🖨️ Print Current Row", command=print_row_data).pack(side="left", padx=8)
    ttk.Button(toolbar_frame, text="💾 Save All Rows", command=save_all).pack(side="left", padx=8)
    ttk.Button(toolbar_frame, text="📂 Load All Rows", command=lambda: load_all(table_frame)).pack(side="left", padx=8)
