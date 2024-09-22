import os
from functions import extensions as ext, folders as f

def create_folders(base_path, isDocsFolder):

    created_folders = set()

    if (isDocsFolder):
        folders = [f.CONTRACTS_FOLDER, f.IDS_FOLDER, f.SIGNINOUT_FOLDER]
    else:
        folders = [f.PRODUCTION_FOLDER, f.POST_PRODUCTION_FOLDER, f.MASTERS_FOLDER]

    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        created_folders.add(folder_path)
        os.makedirs(folder_path, exist_ok=True)

    if not isDocsFolder:
        for subfolder, _ in f.SOURCE_FOLDERS.items():
            folder_path = os.path.join(base_path, f.PRODUCTION_FOLDER, subfolder)
            created_folders.add(folder_path)
            os.makedirs(folder_path, exist_ok=True)

        for subfolder in f.POST_PRODUCTION_SUBFOLDERS:
            folder_path = os.path.join(base_path, f.POST_PRODUCTION_FOLDER, subfolder)
            created_folders.add(folder_path)
            os.makedirs(folder_path, exist_ok=True)

        masters_path = os.path.join(base_path, f.MASTERS_FOLDER)

        for folder in ["Images", "Video"]:
            folder_path = os.path.join(masters_path, folder)
            created_folders.add(folder_path)
            os.makedirs(folder_path, exist_ok=True)

        images_path = os.path.join(masters_path, "Images")

        for subfolder in f.IMAGES_SUBFOLDERS:
            folder_path = os.path.join(images_path, subfolder)
            created_folders.add(folder_path)
            os.makedirs(folder_path, exist_ok=True)

    return created_folders
