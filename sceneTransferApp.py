# Library that allows for folder creation and manipulation.
import os
# Library that supports file copying and removal.
import shutil
# Tcl/Tk library that allows for the graphic user interface.
import tkinter as tk
# Importing the modules necessary for the graphic user interface.
from tkinter import messagebox, filedialog, ttk
# Load the library that allows to read JSON files
import json
from functions import start_organizing as so
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

def main():

    '''
    selected_paths = []
    selected_docs = []
    dummy_path = "/home/nico/Documents/PSM/sceneTransferApp/testScene"
    dummy_docs = "/home/nico/Documents/PSM/sceneTransferApp/testScene/1-Production/docs"
    site_code_entry = ""

    # Create an array that holds the paths the user selected.
    selected_paths.append(dummy_path)
    selected_docs.append(dummy_docs)
    so.start_organizing(selected_paths, selected_docs, site_code_entry)
    '''

    selected_paths = []
    selected_docs = []
    window_title = "Scene Transfer App"
    window_size = "600x500"
    # Call on tkinter and its interpreter to be able to build the
    # graphic user interface (GUI).
    root = tk.Tk()
    # Give the root window in tk a name.
    root.title(window_title)
    # Give the root window dimensions.
    root.geometry(window_size)
    root.configure(bg="white")
    button_color = "white"
    button_borderWidth = 0
    button_highlight = 0
    label_color = "white"
    style = ttk.Style()
    style.configure("Main.TButton",
                    padding=10,
                    borderwidth=0,
                    highlightthickness=0
                   )
    style.map("Main.TButton",
                background=[('active', '#FD6593'), ('!active', '#FEB2C9')]
             )

    folder = tk.PhotoImage(file="icons/folder_white.png")

    def get_restricted_path():
        # Read the restricted path from the text file
        with open("settings/restricted_path.txt", "r") as file:
            return file.readline().strip()  # Read the first line and strip any extra whitespace

    def is_valid_selection(folder_selected, base_path):
        # Get the number of slashes in the base path and the selected folder
        base_depth = base_path.count(os.sep)
        selected_depth = folder_selected.count(os.sep)
        commonPath = os.path.commonpath([folder_selected, base_path])
        # Check if the selected folder is either the base path or exactly one level below it
        if commonPath != base_path or folder_selected == base_path:
            return False
        elif selected_depth >= base_depth + 1:
            return True
        else:
            return False


    # Define a function for folder selection.
    def select_folder():
        base_path = os.path.abspath(get_restricted_path())
        # Prompt the user for a directory and store it in a variable.
        folder_selected = filedialog.askdirectory()
        # If the variable is assigned...
        if folder_selected:
            folder_selected = os.path.abspath(folder_selected)  # Get the absolute path
            if not is_valid_selection(folder_selected, base_path):
                # If the selected folder is at or above the restricted level, show a message box
                messagebox.showerror("Invalid Selection", "Folder selection not allowed at this folder hierarchy. If you wish to select a folder at or above this hierarchy, please change Settings.")
            else:
                # ... include the path the user chose as an element in an array.
                selected_paths.append(folder_selected)
                print(selected_paths)
                # This next line prints the selected folder into the Tk window.
                selected_paths_label.config(text=selected_paths)

    def docs_folder():
        docFolder_selected = filedialog.askdirectory()
        if docFolder_selected:
            selected_docs.append(docFolder_selected)
            selected_docs_label.config(text=selected_docs)


    def clear_selection(clear_scene):
        # Clear the selected paths and reset the label
        if clear_scene:
            selected_paths.clear()
            print(selected_paths)
            selected_paths_label.config(text="No folder selected")
        else:
            selected_docs.clear()
            print(selected_docs)
            selected_docs_label.config(text="No folder selected")



    # Label() implements display boxes where one can place text or images.
    # Here, we place the text specified inside the window.
    # It is not just the title.
    # The first argument
    label = tk.Label(root, text="Organize Scene Files", bg=label_color)
    # pack() has several options for element placement in a tk window.
    # Here, it is used to add padding in the y-axis to the aforementioned text.
    label.pack(pady=10)

    # Create a button using tkinter.  Have it run the "select_folder" function
    # when clicked.
    select_button = ttk.Button(root, image=folder, command=select_folder, style="Main.TButton")
    # Give the button a 10px padding on the y-axis.
    select_button.pack(pady=10)

    # Create a text box for instances where no folder has been selected.
    selected_paths_label = tk.Label(root, text="No folder selected", bg=label_color)
    # Padding.
    selected_paths_label.pack(pady=10)

    # Button to clear the selection
    clear_scene_button = ttk.Button(root, text="Clear Selection", command=lambda: clear_selection(True), style="Main.TButton")
    clear_scene_button.pack(pady=10)

    docs_label = tk.Label(root, text="Select Documents Folder", bg=label_color)
    docs_label.pack(pady=10)

    docs_button = ttk.Button(root, text="Select Docs Folder", command=docs_folder, style="Main.TButton")
    docs_button.pack(pady=10)

    selected_docs_label = tk.Label(root, text="No documents folder selected", bg=label_color)
    selected_docs_label.pack(pady=10)

    clear_docs_button = ttk.Button(root, text="Clear Selection", command=lambda: clear_selection(False), style="Main.TButton")
    clear_docs_button.pack(pady=10)

    site_code_label = tk.Label(root, text="Enter site code", bg=label_color)
    site_code_label.pack(pady=10)

    site_code_entry = tk.Entry(root)
    site_code_entry.pack(pady=10)

    # Create a button to start the process.  We declare "start_organizing()"
    # in this line by using the "lambda" keyword.  It was not previously
    # declared in main().
    start_button = ttk.Button(root, text="Start", command=lambda: so.start_organizing(selected_paths, selected_docs, site_code_entry), style="Main.TButton")
    # Padding
    # Padding
    start_button.pack(pady=10)

    # The infinite loop in tkinter that keeps the program running until the
    # window is closed.
    root.mainloop()


if __name__ == "__main__":
    main()
