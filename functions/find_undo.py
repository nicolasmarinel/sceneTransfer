import json, os, shutil
from functions import original_structure as ogs, organize_files as of, move_files as mf

def undo_reorganization(base_paths):

    for selection in base_paths:
        base_path = selection

    shutil.move(of.moved_doc_path, of.original_doc_path)
    # print(of.created_folders)

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
                # print(dir_path)
                os.rmdir(dir_path)

    for file in mf.duplicate_files:
        directory, full_filename = os.path.split(file)
        counter_file_name, file_ext = os.path.splitext(full_filename)
        og_file_name = counter_file_name[:-4]
        og_file_path = os.path.join(directory, og_file_name + file_ext)
        print(f"OG file path: {og_file_path}")
        os.rename(file, og_file_path)
        # print(f"Renamed {file} -> {og_file_path}")

def find_current_location(file_name, base_path):
    for root, _, files in os.walk(base_path):
        if file_name in files:
            return os.path.join(root, file_name)
    return None
