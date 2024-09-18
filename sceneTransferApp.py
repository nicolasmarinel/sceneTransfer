# Library that allows for folder creation and manipulation.
import os
# Library that supports file copying and removal.
import shutil
# Tcl/Tk library that allows for the graphic user interface.
import tkinter as tk
# Importing the modules necessary for the graphic user interface.
from tkinter import messagebox, filedialog
# Load the library that allows to read JSON files
import json

# Load the JSON file that contains all accepted media file formats.
def load_file_formats(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
# Create a variable that represents the JSON file.
file_formats = load_file_formats('formats.json')

## Create folder names
PRODUCTION_FOLDER = "1-Production"
POST_PRODUCTION_FOLDER = "2-Post_Production"
MASTERS_FOLDER = "3-Masters"
CONTRACTS_FOLDER = "Contracts"
IDS_FOLDER = "IDs"
SIGNINOUT_FOLDER = "SignInOut"

# Arrays that hold file name extensions.
VIDEO_EXTENSIONS = file_formats.get('video', [])
AUDIO_EXTENSIONS = file_formats.get('audio', [])
IMAGE_EXTENSIONS = file_formats.get('images', [])
DOCUMENT_EXTENSIONS = file_formats.get('documents', [])

# Include the arrays with file name extensions inside the source folders.
SOURCE_FOLDERS = {
    "1-Source-Video": VIDEO_EXTENSIONS,
    "2-Source-Audio": AUDIO_EXTENSIONS,
    "3-Source-Images": IMAGE_EXTENSIONS
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

## Create an empty set that will hold the names of all created folders.
created_folders = set()

def create_doc_folders(base_path):
    global created_folders
    folders = [CONTRACTS_FOLDER, IDS_FOLDER, SIGNINOUT_FOLDER]
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        created_folders.add(folder_path)
        os.makedirs(folder_path, exist_ok=True)

## "base_path" is first defined from "folder_selected = filedialog.askdirectory()", which
## then gets appended to the array "selected_paths", and finally, "selected paths" is passed as an argument
## to start_organizing().  start_organizing calls on "organize_files()" and passes "selected_paths" as an argument.
## In turn, "organize_files()" calls on "create_folders()" and passes "base_path" as an argument.
def create_folders(base_path):
    global created_folders
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

            # If the file actually exists in the "Other" folder...
            while os.path.exists(dest_path):
                # Add a suffix to the file name and re-add the file extension.
                new_file_name = f"{file_name} ({counter}){file_ext}"
                dest_path = os.path.join(dest, new_file_name)
                counter += 1
            # This block of code will only execute when the path does not exist yet.
            # Move the file from the original folder to the destination folder.
            shutil.move(file_path, dest_path)
            # print(f"Moved {file_path} to {os.path.join(dest, file)}")


def list_folders(root_folder, extensions):
    found_folders = []
    # List all items in the current folder
    for item in os.listdir(root_folder):
        item_path = os.path.join(root_folder, item)
        # Check if the item is a directory
        if os.path.isdir(item_path):
            for d in os.listdir(item_path):
                if d.lower().endswith(tuple(extensions)):
                    found_folders.append(item_path)
                    break
            # for f in os.listdir(item_path):
            # print(f"Item: {item_path}")
            # Recursively check inside this folder
            found_folders.extend(list_folders(item_path, extensions))
    return found_folders

def organize_docs(doc_path, base_path):
    # Get the parent directory of the documents folder.
    # base_path = os.path.dirname(doc_path)
    # Get the folder level for base path.
    parent_path = os.path.dirname(base_path)
    # Get the docs folder name.
    docs_folder = os.path.basename(doc_path)
    # Create the destination path.
    dest_folder = os.path.join(parent_path, docs_folder)
    # Move the docs folder.
    shutil.move(doc_path, dest_folder)
    print(f"{docs_folder} moved to {parent_path}")

    asset_extensions = VIDEO_EXTENSIONS + IMAGE_EXTENSIONS + DOCUMENT_EXTENSIONS

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

    document_folders = list_folders(dest_folder, DOCUMENT_EXTENSIONS)
    image_folders = list_folders(dest_folder, IMAGE_EXTENSIONS)
    video_folders = list_folders(dest_folder, VIDEO_EXTENSIONS)

    create_doc_folders(dest_folder)

    for folder in document_folders:
        asset_folder = os.path.join(dest_folder, CONTRACTS_FOLDER)
        os.makedirs(asset_folder, exist_ok=True)
        move_files(folder, asset_folder, DOCUMENT_EXTENSIONS)

    asset_folder = os.path.join(dest_folder, CONTRACTS_FOLDER)
    move_files(dest_folder, asset_folder, DOCUMENT_EXTENSIONS)

    for folder in image_folders:
        asset_folder = os.path.join(dest_folder, IDS_FOLDER)
        os.makedirs(asset_folder, exist_ok=True)
        move_files(folder, asset_folder, IMAGE_EXTENSIONS)

    asset_folder = os.path.join(dest_folder, IDS_FOLDER)
    move_files(dest_folder, asset_folder, IMAGE_EXTENSIONS)

    for folder in video_folders:
        asset_folder = os.path.join(dest_folder, SIGNINOUT_FOLDER)
        os.makedirs(asset_folder, exist_ok=True)
        move_files(folder, asset_folder, VIDEO_EXTENSIONS)

    asset_folder = os.path.join(dest_folder, SIGNINOUT_FOLDER)
    move_files(dest_folder, asset_folder, VIDEO_EXTENSIONS)



    for root, dirs, _ in os.walk(dest_folder, topdown=False):
        # For every folder...
        for dir in dirs:
            # ... join the user-selected path with the found folders.
            dir_path = os.path.join(root, dir)
            # If the folder is not a folder created by this program and it's empty...
            if dir_path not in created_folders and not os.listdir(dir_path):
                # ... delete the folder.
                os.rmdir(dir_path)
                print(f"Deleted empty folder: {dir_path}")


# The function that is called with every iteration of the loop inside "start_organizing()"
def organize_files(base_path):

    asset_extensions = VIDEO_EXTENSIONS + AUDIO_EXTENSIONS + IMAGE_EXTENSIONS
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
    video_folders = list_folders(base_path, VIDEO_EXTENSIONS)
    image_folders = list_folders(base_path, IMAGE_EXTENSIONS)
    audio_folders = list_folders(base_path, AUDIO_EXTENSIONS)

    create_folders(base_path)

    # This loop runs once for every folder found with at least one video file
    # inside it.
    for folder in video_folders:
        # The following line creates a path with the same name as the "found"
        # video folder inside "1-Source-Video".  For example, if the found video
        # folder was called "Tree", the path would be:
        # 1-Production/1-Source-Video/Tree
        # In essence, it creates a folder for each found video folder.
        dest_folder = os.path.join(base_path, PRODUCTION_FOLDER, "1-Source-Video", os.path.basename(folder))
        # Now, actually create the folder mentioned in the previous line.
        os.makedirs(dest_folder, exist_ok=True)
        # The function "move_files()" is called upon.
        move_files(folder, dest_folder, VIDEO_EXTENSIONS)
        #print(f"Moved video files from {folder} to {dest_folder}")

    # Same loop as before, but for audio.  This loop does not respect subfolders
    # for source material like the video files loop does.
    for folder in audio_folders:
        dest_folder = os.path.join(base_path, PRODUCTION_FOLDER, "2-Source-Audio")
        os.makedirs(dest_folder, exist_ok=True)
        move_files(folder, dest_folder, AUDIO_EXTENSIONS)
        #print(f"Moved video files from {folder} to {dest_folder}")

    # Same loop as before, but for images.
    for folder in image_folders:
        dest_folder = os.path.join(base_path, PRODUCTION_FOLDER, "3-Source-Images")
        os.makedirs(dest_folder, exist_ok=True)
        move_files(folder, dest_folder, IMAGE_EXTENSIONS)
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
                print(f"Deleted empty folder: {dir_path}")


# The function called when the user presses the "Start" button.
def start_organizing(base_paths, doc_paths, site_code_entry):

    site_code = site_code_entry.get()

    for selection in base_paths:
        base_path = selection
    for selection in doc_paths:
        doc_path = selection

    organize_docs(doc_path, base_path)
    organize_files(base_path)

    messagebox.showinfo("Done", "Files have been organized successfully.")




def main():
    '''
    dummy_path = "/home/nico/Documents/PSM/Ingest Organizer/dummy"
    # create_folders(dummy_path)

    # Create an array that holds the paths the user selected.
    selected_paths.append(dummy_path)
    start_organizing(selected_paths)
    '''

    selected_paths = []
    selected_docs = []
    window_title = "Organize Scene Files"
    window_size = "400x400"
    # Call on tkinter and its interpreter to be able to build the
    # graphic user interface (GUI).
    root = tk.Tk()
    # Give the root window in tk a name.
    root.title(window_title)
    # Give the root window dimensions.
    root.geometry(window_size)

    # Define a function for folder selection.
    def select_folder():
        # Prompt the user for a directory and store it in a variable.
        folder_selected = filedialog.askdirectory()
        # If the variable is assigned...
        if folder_selected:
            # ... include the path the user chose as an element in an array.
            selected_paths.append(folder_selected)
            # This next line prints the selected folder into the Tk window.
            selected_paths_label.config(text=selected_paths)

    def docs_folder():
        docFolder_selected = filedialog.askdirectory()
        if docFolder_selected:
            selected_docs.append(docFolder_selected)
            selected_docs_label.config(text=selected_docs)


    # Label() implements display boxes where one can place text or images.
    # Here, we place the text specified inside the window.
    # It is not just the title.
    # The first argument
    label = tk.Label(root, text="Organize Scene Files")
    # pack() has several options for element placement in a tk window.
    # Here, it is used to add padding in the y-axis to the aforementioned text.
    label.pack(pady=10)

    # Create a button using tkinter.  Have it run the "select_folder" function
    # when clicked.
    select_button = tk.Button(root, text="Select Folder", command=select_folder)
    # Give the button a 10px padding on the y-axis.
    select_button.pack(pady=10)

    # Create a text box for instances where no folder has been selected.
    selected_paths_label = tk.Label(root, text="No folder selected")
    # Padding.
    selected_paths_label.pack(pady=10)

    docs_label = tk.Label(root, text="Select Documents Folder")
    docs_label.pack(pady=10)

    docs_button = tk.Button(root, text="Select Docs Folder", command=docs_folder)
    docs_button.pack(pady=10)

    selected_docs_label = tk.Label(root, text="No documents folder selected")
    selected_docs_label.pack(pady=10)

    site_code_label = tk.Label(root, text="Enter site code")
    site_code_label.pack(pady=10)

    site_code_entry = tk.Entry(root)
    site_code_entry.pack(pady=10)

    # Create a button to start the process.  We declare "start_organizing()"
    # in this line by using the "lambda" keyword.  It was not previously
    # declared in main().
    start_button = tk.Button(root, text="Start", command=lambda: start_organizing(selected_paths, selected_docs, site_code_entry))
    # Padding
    # Padding
    start_button.pack(pady=10)

    # The infinite loop in tkinter that keeps the program running until the
    # window is closed.
    root.mainloop()


if __name__ == "__main__":
    main()
