import os
from functions import extensions as ext

## Create folder names
PRODUCTION_FOLDER = "1-Production"
POST_PRODUCTION_FOLDER = "2-Post_Production"
MASTERS_FOLDER = "3-Masters"

# Include the arrays with file name extensions inside the source folders.
SOURCE_FOLDERS = {
    "1-Source-Video": ext.VIDEO_EXTENSIONS,
    "2-Source-Audio": ext.AUDIO_EXTENSIONS,
    "3-Source-Images": ext.IMAGE_EXTENSIONS
}

POST_PRODUCTION_SUBFOLDERS = [
    "0-Project_Files",
    "1-Edit-Video",
    "2-Edit-Audio",
    "3-Edit-Images",
    "4-Edit-Graphics"
]

IMAGES_SUBFOLDERS = [
    "Final_Retouches",
    "Pictures_HD",
    "Screencaps"
]

## "base_path" is first defined from "folder_selected = filedialog.askdirectory()", which
## then gets appended to the array "selected_paths", and finally, "selected paths" is passed as an argument
## to start_organizing().  start_organizing calls on "organize_files()" and passes "selected_paths" as an argument.
## In turn, "organize_files()" calls on "create_folders()" and passes "base_path" as an argument.
def create_folders(base_path):
    created_folders = set()
    main_folders = [PRODUCTION_FOLDER, POST_PRODUCTION_FOLDER, MASTERS_FOLDER]
    # For each folder in the array "main_folders"
    for folder in main_folders:
        # Join the user-provided path with each folder name in the above-defined arrays.
        folder_path = os.path.join(base_path, folder)
        # Add the path defined in this iteration to the array "created_folders"
        created_folders.add(folder_path)
        # Call on the operating system to create the folders.
        os.makedirs(folder_path, exist_ok=True)
        # Let the user know a folder was created.
        # print(f"Created folder: {folder_path}")

    # Create a loop around the items contained within the array "SOURCE_FOLDERS"
    # The items() function is necessary because the items inside "SOURCE_FOLDERS"
    # contain key-value pairs.
    for subfolder, _ in SOURCE_FOLDERS.items():
        folder_path = os.path.join(base_path, PRODUCTION_FOLDER, subfolder)
        created_folders.add(folder_path)
        os.makedirs(folder_path, exist_ok=True)
        # print(f"Created folder: {folder_path}")

    # This loops repeats the same process for the "2-Post_Production" subfolders.
    for subfolder in POST_PRODUCTION_SUBFOLDERS:
        folder_path = os.path.join(base_path, POST_PRODUCTION_FOLDER, subfolder)
        created_folders.add(folder_path)
        os.makedirs(folder_path, exist_ok=True)
        # print(f"Created folder: {folder_path}")

    # Join the user-provided path with the name for the "3-Masters" folder.
    masters_path = os.path.join(base_path, MASTERS_FOLDER)
    # This loops repeats the same process for the "3-Masters" subfolders.
    # The difference here is the folders are named here, not in an external variable.
    for folder in ["Images", "Video"]:
        folder_path = os.path.join(masters_path, folder)
        created_folders.add(folder_path)
        os.makedirs(folder_path, exist_ok=True)
        # print(f"Created folder: {folder_path}")

    # Place the "Images" text after the path to the "3-Masters" folder.
    images_path = os.path.join(masters_path, "Images")
    # Loop that created folders contained in the array "IMAGES_SUBFOLDERS".
    for subfolder in IMAGES_SUBFOLDERS:
        folder_path = os.path.join(images_path, subfolder)
        created_folders.add(folder_path)
        os.makedirs(folder_path, exist_ok=True)
        # print(f"Created folder: {folder_path}")

    return created_folders
