import os, json
from functions import extensions as ext, folders as f

# This function creates folders where the found files will be reorganized to.
def create_folders(base_path, isDocsFolder=None, moved_doc_path=None):

    # This is a set of all the folders that will be created.
    created_folders = set()

    # This is the list of folders that will be created if the document path is present.
    # These folders can be found within 'folders.py'.
    if isDocsFolder:
        folders = [f.CONTRACTS_FOLDER, f.IDS_FOLDER, f.SIGNINOUT_FOLDER]
    # This is the list of folders that will be created if the document path is not present.
    else:
        folders = [f.PRODUCTION_FOLDER, f.POST_PRODUCTION_FOLDER, f.MASTERS_FOLDER]

    # Whatever was passed into "folders" by the previous 'if' statement, use it to create
    # the main folder structure.
    # For all the folders in the "folders" array...
    for folder in folders:
        # Create the path for the folder.
        folder_path = os.path.join(base_path, folder)
        # Add the folder to the set of created folders.
        if isDocsFolder:
            created_folders.add(os.path.join(moved_doc_path, folder))
        else:
            created_folders.add(folder_path)
        # Actually create the folder.
        os.makedirs(folder_path, exist_ok=True)

    # If this is not a document path, then create the folders listed in 'folders.py' for production folders.
    if not isDocsFolder:
        # For all the 
        for subfolder, _ in f.SOURCE_FOLDERS.items():
            # Create the path for the "1-Production" folder.
            folder_path = os.path.join(base_path, f.PRODUCTION_FOLDER, subfolder)
            # Add the folder to the set of created folders.
            created_folders.add(folder_path)
            # Actually create the folder.
            os.makedirs(folder_path, exist_ok=True)

        # This is the same as above, but for the "2-Production Folder"
        for subfolder in f.POST_PRODUCTION_SUBFOLDERS:
            folder_path = os.path.join(base_path, f.POST_PRODUCTION_FOLDER, subfolder)
            created_folders.add(folder_path)
            os.makedirs(folder_path, exist_ok=True)

        # Create the path for the "3-Edit-Images" folder.
        post_images_path = os.path.join(base_path, f.POST_PRODUCTION_FOLDER, f.POST_PRODUCTION_SUBFOLDERS[3]) 

        # Create the path for the "3-Masters" folder.  
        masters_path = os.path.join(base_path, f.MASTERS_FOLDER)

        # Place the "Images" and "Video" folders inside the "3-Masters" folder.
        # We will consider moving this to the "folders.py" file.  
        # I see no reason why this wasn't declared in that file.
        for folder in ["Images", "Video"]:
            folder_path = os.path.join(masters_path, folder)
            created_folders.add(folder_path)
            os.makedirs(folder_path, exist_ok=True)

        # Create the "Images" subfolder.
        images_path = os.path.join(masters_path, "Images")

        for subfolder in f.IMAGE_MASTERS_SUBFOLDERS:
            folder_path = os.path.join(images_path, subfolder)
            created_folders.add(folder_path)
            os.makedirs(folder_path, exist_ok=True)
        
        for subfolder in f.IMAGE_POST_SUBFOLDERS:
            folder_path = os.path.join(post_images_path, subfolder)
            created_folders.add(folder_path)
            os.makedirs(folder_path, exist_ok=True)

    # Convert set to list for JSON serialization
    created_folders_list = list(created_folders)
    with open("created_folders_function.json", "w") as createdJson:
        json.dump(created_folders_list, createdJson, indent=4)

    return created_folders
