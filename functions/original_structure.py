import os
import json

original_structure = {}

def log_original_structure(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            original_structure[file] = file_path
    with open("original_structure.json", "w") as f:
        json.dump(original_structure, f)
