import json, os, shutil
from functions import original_structure as ogs, organize_files as of

def undo_reorganization(base_paths):

    for selection in base_paths:
        base_path = selection

    shutil.move(of.moved_doc_path, of.original_doc_path)
    print(of.created_folders)

    try:
        with open("original_structure.json", "r") as f:
            original_structure = json.load(f)

        directories = original_structure.get("directories", [])
        original_paths = original_structure.get("files", [])

        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                print(f"Error creating {directory}: {e}")

        for original_path in original_paths:
            file_name = os.path.basename(original_path)
            current_location = find_current_location(file_name, base_path)
            if current_location:
                shutil.move(current_location, original_path)

        print("Undo successful. Files restored to their original structure.")

    except Exception as e:
        print("Error restoring files:", e)

    for root, dirs, _ in os.walk(base_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir_path in of.created_folders and not os.listdir(dir_path):
                print(dir_path)
                os.rmdir(dir_path)

def find_current_location(file_name, base_path):
    for root, _, files in os.walk(base_path):  # Replace with your folder variable
        if file_name in files:
            return os.path.join(root, file_name)
    return None
