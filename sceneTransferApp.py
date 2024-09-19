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
from functions import start_organizing as so

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
    start_button = tk.Button(root, text="Start", command=lambda: so.start_organizing(selected_paths, selected_docs, site_code_entry))
    # Padding
    # Padding
    start_button.pack(pady=10)

    # The infinite loop in tkinter that keeps the program running until the
    # window is closed.
    root.mainloop()


if __name__ == "__main__":
    main()
