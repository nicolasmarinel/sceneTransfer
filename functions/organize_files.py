import os, shutil, json
from functions import extensions as ext, list_folders as lf, create_folders as cf, move_files as mf, folders as f

created_folders = []
original_doc_path = ""
moved_doc_path = ""

def organize_files(base_path, doc_path=None, multicam=None, imgFolders=None):

    global created_folders

    # All the behavior changes for when a doc. path is present.
    if doc_path:
        # The following three are for moving the document path one directory up.
        global original_doc_path
        global moved_doc_path
        # Store the original document path in a variable.
        original_doc_path = doc_path
        isDocsFolder = True
        # Get the directory right above the scene folder.
        parent_path = os.path.dirname(base_path)
        # Get the name of the documetns folder.
        docs_folder_name = os.path.basename(doc_path)
        # Create a path for the documents folder at the same level as the scene's parent folder.
        dest_folder = os.path.join(parent_path, docs_folder_name)
        # Store the place the document folder was moved to in a variable.
        moved_doc_path = dest_folder
        # The folder extensions to be used in a document path.
        asset_extensions = ext.VIDEO_EXTENSIONS + ext.IMAGE_EXTENSIONS + ext.DOCUMENT_EXTENSIONS
        # The base path to be used is the doc path for the remainder of the function.
        base_path = doc_path
    else:
        isDocsFolder = False
        # If this is not a document path, then use the extension that involve audio.
        asset_extensions = ext.VIDEO_EXTENSIONS + ext.AUDIO_EXTENSIONS + ext.IMAGE_EXTENSIONS

    # Create the path for the "Other" folder.
    other = os.path.join(base_path, "Other")
    # Store the "Other" folder in the list of created folders.
    created_folders.append(other)
    # Create the "Other" folder.
    os.makedirs(other, exist_ok=True)

    # The main loop for organizing the files.
    for root, dirs, files in os.walk(base_path, topdown=False):
        # Walk the base path and remove any files that start with a dot.
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            if file.startswith("."):
                os.remove(file_path)
                continue
            # Check if the file extension is in the list of asset extensions.
            for idx, extension in enumerate(asset_extensions):
                # If the file extension is in the list of asset extensions, then leave it alone.
                if file_ext.endswith(extension):
                    break
                # If the file extension is not in the list of asset extensions, then move it to the "Other" folder.
                if idx == len(asset_extensions)-1:
                    dest_path = os.path.join(other, file)
                    file_name = os.path.splitext(file)[0]
                    # If the file already exists in the "Other" folder, then rename it.
                    # We first set a counter to keep track of the number of times we've renamed the file.
                    # This is because multiple files with the same name can exist in different folders.
                    counter = 1
                    while os.path.exists(dest_path):
                        # We then rename the file by adding a number to the end of the file name.
                        new_file_name = f"{file_name} ({counter}){file_ext}"
                        dest_path = os.path.join(other, new_file_name)
                        # Increase the counter so, if we find another file with the same name, it will take on the next number.
                        counter += 1
                    # Move the file to the "Other" folder.
                    shutil.move(os.path.join(root, file), dest_path)

    # List all folders found with files inside them that match video extensions.
    video_folders = lf.list_folders(base_path, ext.VIDEO_EXTENSIONS)
    # List all folders found with files inside them that match image extensions.
    image_folders = lf.list_folders(base_path, ext.IMAGE_EXTENSIONS)
    # If the document path is present, then list all folders found with files inside them that match document extensions.
    if isDocsFolder:
        document_folders = lf.list_folders(doc_path, ext.DOCUMENT_EXTENSIONS)
    # If the document path is not present, then list all folders found with files inside them that match audio extensions.
    else:
        audio_folders = lf.list_folders(base_path, ext.AUDIO_EXTENSIONS)

    # Create the folders all assets will be moved to as defined by the user.
    if isDocsFolder:
        folders_created = cf.create_folders(base_path, isDocsFolder, moved_doc_path)
    else:
        folders_created = cf.create_folders(base_path)
    # Keep a list of all the folders that have been created thus far.
    created_folders.extend(folders_created)
    # Keep that log of created folders in a JSON file.
    with open("created_folders_of.json", "w") as createdJson:
        json.dump(created_folders, createdJson, indent=4)

    # For every folder found with video files inside...    
    for folder in video_folders:
        # If this is the documents folder, create a path for the "SignInOut" folder.
        if isDocsFolder:
            asset_folder = os.path.join(base_path, f.SIGNINOUT_FOLDER)
        # If this is not a documents folder, then create a path for the "1-Source-Video folder".
        # Consider if the user selected this as a multicam scene or not.
        # If the user did consider it a multicam scene, respect the different camera folders found.
        else:
            asset_folder = os.path.join(base_path, f.PRODUCTION_FOLDER, "1-Source-Video", os.path.basename(folder) if multicam else "")
        # Add the folders to the created folder list.
        # created_folders.append(asset_folder)
        # Actually create the folders.
        os.makedirs(asset_folder, exist_ok=True)
        # Actually move the files into the video folder, whether "1-Source-Video" or "SignInOut".
        mf.move_files(folder, asset_folder, ext.VIDEO_EXTENSIONS)
    if isDocsFolder:
        # Now that the "SignInout" folder has been created, move whatever video file
        # is directly within the user-selected "Documents" folder (not a subfolder)
        # into the "SignInOut" folder.
        asset_folder = os.path.join(doc_path, f.SIGNINOUT_FOLDER)
        mf.move_files(doc_path, asset_folder, ext.VIDEO_EXTENSIONS)
    
    # Repeat the same process as with the video files, but with image files.
    for folder in image_folders:
        if isDocsFolder:
            asset_folder = os.path.join(base_path, f.IDS_FOLDER)
        else:
            asset_folder = os.path.join(base_path, f.PRODUCTION_FOLDER, "3-Source-Images", os.path.basename(folder) if imgFolders else "")
        os.makedirs(asset_folder, exist_ok=True)
        mf.move_files(folder, asset_folder, ext.IMAGE_EXTENSIONS)
    if isDocsFolder:
        asset_folder = os.path.join(base_path, f.IDS_FOLDER)
        mf.move_files(base_path, asset_folder, ext.IMAGE_EXTENSIONS)

    # Repeat the same process, but with document and audio files.
    if isDocsFolder:
        # For every folder where a document file extension was found in...
        for folder in document_folders:
            # Create a path that points to the selected document path and the "Contracts" folder within it.
            asset_folder = os.path.join(base_path, f.CONTRACTS_FOLDER)
            # Actually create the folder.
            os.makedirs(asset_folder, exist_ok=True)
            # Move all document files to the "Contracts" folder.
            mf.move_files(folder, asset_folder, ext.DOCUMENT_EXTENSIONS)
        # Move any document files at the selected document path level into the "Contracts" folder as well.
        asset_folder = os.path.join(base_path, f.CONTRACTS_FOLDER)
        mf.move_files(doc_path, asset_folder, ext.DOCUMENT_EXTENSIONS)
    else:
        # If this is not a documents folder, then move the audio files.
        # For every folder found with an audio file within it...
        for folder in audio_folders:
            # Create a path that points to the "2-Source-Audio" folder within the "1-Production" folder.
            asset_folder = os.path.join(base_path, f.PRODUCTION_FOLDER, "2-Source-Audio")
            # Actually create the folders.
            os.makedirs(asset_folder, exist_ok=True)
            # Move all audio files to the audio files folder.
            mf.move_files(folder, asset_folder, ext.AUDIO_EXTENSIONS)

    # Move the documents folder from its location inside the scene folder to the same level as the 
    # scene folder.
    if doc_path:
        shutil.move(doc_path, dest_folder)

    # Walk the selected folder and delete any folders not created by the user.
    for root, dirs, _ in os.walk(moved_doc_path if isDocsFolder else base_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir_path not in created_folders and not os.listdir(dir_path):
                os.rmdir(dir_path)
