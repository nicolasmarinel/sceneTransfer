import os, shutil
from functions import extensions as ext, list_folders as lf, create_folders as cf, move_files as mf

# The function that is called with every iteration of the loop inside "start_organizing()"
def organize_files(base_path):

    asset_extensions = ext.VIDEO_EXTENSIONS + ext.AUDIO_EXTENSIONS + ext.IMAGE_EXTENSIONS
    # The path to the "Other" folder.
    other = os.path.join(base_path, "Other")
    os.makedirs(other, exist_ok=True)

    # "root" is the folder or subfolder being searched in an iteration.
    # "dirs" are the sub-folders of the user-selected path
    # "files" are each individual file in the folder.
    for root, dirs, files in os.walk(base_path, topdown=False):
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




    # This function replaces the previous assignment of "video_folders" ChatGPT made.
    video_folders = lf.list_folders(base_path, ext.VIDEO_EXTENSIONS)
    image_folders = lf.list_folders(base_path, ext.IMAGE_EXTENSIONS)
    audio_folders = lf.list_folders(base_path, ext.AUDIO_EXTENSIONS)

    created_folders = cf.create_folders(base_path)

    # This loop runs once for every folder found with at least one video file
    # inside it.
    for folder in video_folders:
        # The following line creates a path with the same name as the "found"
        # video folder inside "1-Source-Video".  For example, if the found video
        # folder was called "Tree", the path would be:
        # 1-Production/1-Source-Video/Tree
        # In essence, it creates a folder for each found video folder.
        dest_folder = os.path.join(base_path, cf.PRODUCTION_FOLDER, "1-Source-Video", os.path.basename(folder))
        # Now, actually create the folder mentioned in the previous line.
        os.makedirs(dest_folder, exist_ok=True)
        # The function "mf.move_files()" is called upon.
        mf.move_files(folder, dest_folder, ext.VIDEO_EXTENSIONS)
        #print(f"Moved video files from {folder} to {dest_folder}")

    # Same loop as before, but for audio.  This loop does not respect subfolders
    # for source material like the video files loop does.
    for folder in audio_folders:
        dest_folder = os.path.join(base_path, cf.PRODUCTION_FOLDER, "2-Source-Audio")
        os.makedirs(dest_folder, exist_ok=True)
        mf.move_files(folder, dest_folder, ext.AUDIO_EXTENSIONS)
        #print(f"Moved video files from {folder} to {dest_folder}")

    # Same loop as before, but for images.
    for folder in image_folders:
        dest_folder = os.path.join(base_path, cf.PRODUCTION_FOLDER, "3-Source-Images")
        os.makedirs(dest_folder, exist_ok=True)
        mf.move_files(folder, dest_folder, ext.IMAGE_EXTENSIONS)
        #print(f"Moved video files from {folder} to {dest_folder}")

    # "root" represents a full path name, such as:
    # /home/nico/Documents/PSM/Ingest Organizer/dummy/VIDEO/
    # "dirs" represents a list of subfolders in that directory, such as
    # ['Cam 1', 'bCAM X']
    # "_" represents a list of files, such as
    # ['video1.mp4', 'video2.mp4']
    # The walk() function analyzes all folders and files inside the user-selected
    # folder.
    for root, dirs, _ in os.walk(base_path, topdown=False):
        # For every folder...
        for dir in dirs:
            # ... join the user-selected path with the found folders.
            dir_path = os.path.join(root, dir)
            # If the folder is not a folder created by this program and it's empty...
            if dir_path not in created_folders and not os.listdir(dir_path):
                # ... delete the folder.
                os.rmdir(dir_path)
                # print(f"Deleted empty folder: {dir_path}")
