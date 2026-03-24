import json
from tkinter import filedialog

def save_data(data):
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Data saved to {file_path}")
        except Exception as e:
            print(f"Error saving data: {e}")

def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            print(f"Loaded data from {file_path}")
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}
    return {}

def save_all_rows(data_list):
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'w') as f:
                json.dump(data_list, f, indent=4)
            print(f" All rows saved to {file_path}")
        except Exception as e:
            print(f" Error saving all rows: {e}")

def load_all_rows():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'r') as f:
                data_list = json.load(f)
            print(f" Loaded {len(data_list)} rows from {file_path}")
            return data_list
        except Exception as e:
            print(f" Error loading all rows: {e}")
            return []
    return []
