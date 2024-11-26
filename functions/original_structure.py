import os
import json

original_structure = {
    "directories": [],
    "files": []
}

def log_original_structure(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            original_structure["directories"].append(dir_path)
        for file in files:
            file_path = os.path.join(root, file)
            original_structure["files"].append(file_path)
    with open("original_structure.json", "w") as f:
        json.dump(original_structure, f, indent=4)
