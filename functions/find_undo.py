import json, os, shutil
from functions import original_structure as ogs

def undo_reorganization(base_paths):

    for selection in base_paths:
        base_path = selection

    try:
        with open("original_structure.json", "r") as f:
            original_structure = json.load(f)

        for file, original_path in original_structure.items():
            current_location = find_current_location(file, base_path)
            if current_location:
                shutil.move(current_location, original_path)

        print("Undo successful. Files restored to their original structure.")
    except Exception as e:
        print("Error restoring files:", e)

def find_current_location(file_name, base_path):
    for root, _, files in os.walk(base_path):  # Replace with your folder variable
        if file_name in files:
            return os.path.join(root, file_name)
    return None
