import os, shutil, json

json_file_path = 'original_structure.json'
duplicate_files = []

def move_files(src, dest, file_exts):

    if os.path.exists(json_file_path):
        with open (json_file_path, 'r') as og_struct_json:
            og_structure = json.load(og_struct_json)

    # For each item found inside the folder...
    for file in os.listdir(src):
        # ... get the original file path before moving.
        file_path = os.path.join(src, file)
        # If what is found in the path is a file,
        # and the file path ends with any of the file extensions listed
        # in the corresponding tuple...
        if os.path.isfile(file_path) and file.lower().endswith(tuple(file_exts)):
            # Check if the current file already exists in the folder.
            dest_path = os.path.join(dest, file)
            file_name = os.path.splitext(file)[0]
            file_ext = os.path.splitext(file)[1].lower()

            counter = 1
            # If the file actually exists in the folder...
            while os.path.exists(dest_path):
                # Add a suffix to the file name and re-add the file extension.
                new_file_name = f"{file_name} ({counter}){file_ext}"
                dest_path = os.path.join(dest, new_file_name)

                if file_path in og_structure["files"]:
                    #print(f"{file_path} found in JSON file.")
                    index = og_structure["files"].index(file_path)
                    og_structure["files"][index] = os.path.join(os.path.dirname(file_path), new_file_name)
                    duplicate_files.append(og_structure["files"][index])
                    #print(duplicate_files)
                    with open('original_structure.json', 'w') as og_struct_json:
                        json.dump(og_structure, og_struct_json, indent=4)
                else:
                    print("File path not found in JSON file.")

                counter += 1
            # This block of code will only execute when the path does not exist yet.
            # Move the file from the original folder to the destination folder.
            shutil.move(file_path, dest_path)
            # print(f"Moved {file_path} to {os.path.join(dest, file)}")
