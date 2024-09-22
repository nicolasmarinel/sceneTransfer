import os, shutil
from functions import extensions as ext, list_folders as lf, create_folders as cf, move_files as mf, folders as f

def organize_files(base_path, doc_path=None):

    if doc_path:
        isDocsFolder = True
        parent_path = os.path.dirname(base_path)
        docs_folder = os.path.basename(doc_path)
        dest_folder = os.path.join(parent_path, docs_folder)
        shutil.move(doc_path, dest_folder)
        asset_extensions = ext.VIDEO_EXTENSIONS + ext.IMAGE_EXTENSIONS + ext.DOCUMENT_EXTENSIONS
        base_path = dest_folder
    else:
        isDocsFolder = False
        asset_extensions = ext.VIDEO_EXTENSIONS + ext.AUDIO_EXTENSIONS + ext.IMAGE_EXTENSIONS

    other = os.path.join(base_path, "Other")
    os.makedirs(other, exist_ok=True)

    for root, dirs, files in os.walk(base_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            if file.startswith("."):
                os.remove(file_path)
                continue
            for idx, extension in enumerate(asset_extensions):
                if file_ext.endswith(extension):
                    break
                if idx == len(asset_extensions)-1:
                    dest_path = os.path.join(other, file)
                    file_name = os.path.splitext(file)[0]
                    counter = 1
                    while os.path.exists(dest_path):
                        new_file_name = f"{file_name} ({counter}){file_ext}"
                        dest_path = os.path.join(other, new_file_name)
                        counter += 1
                    shutil.move(os.path.join(root, file), dest_path)

    video_folders = lf.list_folders(base_path, ext.VIDEO_EXTENSIONS)
    image_folders = lf.list_folders(base_path, ext.IMAGE_EXTENSIONS)
    if isDocsFolder:
        document_folders = lf.list_folders(dest_folder, ext.DOCUMENT_EXTENSIONS)
    else:
        audio_folders = lf.list_folders(base_path, ext.AUDIO_EXTENSIONS)

    created_folders = cf.create_folders(base_path, isDocsFolder)

    for folder in video_folders:
        if isDocsFolder:
            asset_folder = os.path.join(base_path, f.SIGNINOUT_FOLDER)
        else:
            asset_folder = os.path.join(base_path, f.PRODUCTION_FOLDER, "1-Source-Video", os.path.basename(folder))
        os.makedirs(asset_folder, exist_ok=True)
        mf.move_files(folder, asset_folder, ext.VIDEO_EXTENSIONS)
    if isDocsFolder:
        asset_folder = os.path.join(dest_folder, f.SIGNINOUT_FOLDER)
        mf.move_files(dest_folder, asset_folder, ext.VIDEO_EXTENSIONS)

    for folder in image_folders:
        if isDocsFolder:
            asset_folder = os.path.join(base_path, f.IDS_FOLDER)
        else:
            asset_folder = os.path.join(base_path, f.PRODUCTION_FOLDER, "3-Source-Images")
        os.makedirs(asset_folder, exist_ok=True)
        mf.move_files(folder, asset_folder, ext.IMAGE_EXTENSIONS)
    if isDocsFolder:
        asset_folder = os.path.join(base_path, f.IDS_FOLDER)
        mf.move_files(base_path, asset_folder, ext.IMAGE_EXTENSIONS)

    if isDocsFolder:
        for folder in document_folders:
            asset_folder = os.path.join(base_path, f.CONTRACTS_FOLDER)
            os.makedirs(asset_folder, exist_ok=True)
            mf.move_files(folder, asset_folder, ext.DOCUMENT_EXTENSIONS)
        asset_folder = os.path.join(base_path, f.CONTRACTS_FOLDER)
        mf.move_files(dest_folder, asset_folder, ext.DOCUMENT_EXTENSIONS)
    else:
        for folder in audio_folders:
            dest_folder = os.path.join(base_path, f.PRODUCTION_FOLDER, "2-Source-Audio")
            os.makedirs(dest_folder, exist_ok=True)
            mf.move_files(folder, dest_folder, ext.AUDIO_EXTENSIONS)

    for root, dirs, _ in os.walk(base_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir_path not in created_folders and not os.listdir(dir_path):
                os.rmdir(dir_path)
