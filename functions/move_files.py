import os, shutil

# This function moves all video files into the "video" folder.
# It takes in a source folder, a destionation folder, and the file extensions
# it's supposed to look for.
def move_files(src, dest, file_exts):
    # For each item found inside the found video files folder...
    for file in os.listdir(src):
        # ... get the original file path before moving.
        file_path = os.path.join(src, file)
        # If the what is found in the path is a file, meaning a video file
        # and the file path ends with any of the video file extensions listed
        # in the VIDEO_EXTENSIONS tuple...
        if os.path.isfile(file_path) and file.lower().endswith(tuple(file_exts)):
            # Check if the current file already exists in the "Other" folder.
            dest_path = os.path.join(dest, file)
            file_name = os.path.splitext(file)[0]
            file_ext = os.path.splitext(file)[1].lower()

            counter = 1
            # If the file actually exists in the folder...
            while os.path.exists(dest_path):
                # Add a suffix to the file name and re-add the file extension.
                new_file_name = f"{file_name} ({counter}){file_ext}"
                dest_path = os.path.join(dest, new_file_name)
                counter += 1
            # This block of code will only execute when the path does not exist yet.
            # Move the file from the original folder to the destination folder.
            shutil.move(file_path, dest_path)
            # print(f"Moved {file_path} to {os.path.join(dest, file)}")
