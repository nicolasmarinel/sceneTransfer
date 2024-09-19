import os, shutil
from functions import extensions as ext, list_folders as lf, create_doc_folders as cdf, move_files as mf

def organize_docs(doc_path, base_path):
    # Get the folder level for base path.
    parent_path = os.path.dirname(base_path)
    # Get the docs folder name.
    docs_folder = os.path.basename(doc_path)
    # Create the destination path.
    dest_folder = os.path.join(parent_path, docs_folder)
    # Move the docs folder.
    shutil.move(doc_path, dest_folder)
    # print(f"{docs_folder} moved to {parent_path}")

    asset_extensions = ext.VIDEO_EXTENSIONS + ext.IMAGE_EXTENSIONS + ext.DOCUMENT_EXTENSIONS

    other = os.path.join(dest_folder, "Other")
    os.makedirs(other, exist_ok=True)

    for root, dirs, files in os.walk(dest_folder, topdown=False):
        for file in files:
            # The complete path to the specific file.
            file_path = os.path.join(root, file)
            # The file extension of the file.
            file_ext = os.path.splitext(file)[1].lower()
            # Delete if the file begins with a period.
            if file.startswith("."):
                os.remove(file_path)
                continue
            # Ignore if the file extension is one of the video assets.
            for idx, extension in enumerate(asset_extensions):
                if file_ext.endswith(extension):
                    break
                if idx == len(asset_extensions)-1:
                    # Check if the current file already exists in the "Other" folder.
                    dest_path = os.path.join(other, file)
                    file_name = os.path.splitext(file)[0]

                    counter = 1

                    # If the file actually exists in the "Other" folder...
                    while os.path.exists(dest_path):
                        # Add a suffix to the file name and re-add the file extension.
                        new_file_name = f"{file_name} ({counter}){file_ext}"
                        dest_path = os.path.join(other, new_file_name)
                        counter += 1
                    # This block of code will only execute when the path does not exist yet.
                    shutil.move(os.path.join(root, file), dest_path)

    document_folders = lf.list_folders(dest_folder, ext.DOCUMENT_EXTENSIONS)
    image_folders = lf.list_folders(dest_folder, ext.IMAGE_EXTENSIONS)
    video_folders = lf.list_folders(dest_folder, ext.VIDEO_EXTENSIONS)

    created_folders = cdf.create_doc_folders(dest_folder)

    for folder in document_folders:
        asset_folder = os.path.join(dest_folder, cdf.CONTRACTS_FOLDER)
        os.makedirs(asset_folder, exist_ok=True)
        mf.move_files(folder, asset_folder, ext.DOCUMENT_EXTENSIONS)

    asset_folder = os.path.join(dest_folder, cdf.CONTRACTS_FOLDER)
    mf.move_files(dest_folder, asset_folder, ext.DOCUMENT_EXTENSIONS)

    for folder in image_folders:
        asset_folder = os.path.join(dest_folder, cdf.IDS_FOLDER)
        os.makedirs(asset_folder, exist_ok=True)
        mf.move_files(folder, asset_folder, ext.IMAGE_EXTENSIONS)

    asset_folder = os.path.join(dest_folder, cdf.IDS_FOLDER)
    mf.move_files(dest_folder, asset_folder, ext.IMAGE_EXTENSIONS)

    for folder in video_folders:
        asset_folder = os.path.join(dest_folder, cdf.SIGNINOUT_FOLDER)
        os.makedirs(asset_folder, exist_ok=True)
        mf.move_files(folder, asset_folder, ext.VIDEO_EXTENSIONS)

    asset_folder = os.path.join(dest_folder, cdf.SIGNINOUT_FOLDER)
    mf.move_files(dest_folder, asset_folder, ext.VIDEO_EXTENSIONS)



    for root, dirs, _ in os.walk(dest_folder, topdown=False):
        # For every folder...
        for dir in dirs:
            # ... join the user-selected path with the found folders.
            dir_path = os.path.join(root, dir)
            # If the folder is not a folder created by this program and it's empty...
            if dir_path not in created_folders and not os.listdir(dir_path):
                # ... delete the folder.
                os.rmdir(dir_path)
                # print(f"Deleted empty folder: {dir_path}")
