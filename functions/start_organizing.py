from functions import organize_files as of, original_structure as ogs
# Importing the modules necessary for the graphic user interface.
from tkinter import messagebox

# The function called when the user presses the "Start" button.
def start_organizing(base_paths, doc_paths):

    #site_code = site_code_entry.get()
    #print(site_code)

    for selection in base_paths:
        base_path = selection
    for selection in doc_paths:
        doc_path = selection

    ogs.log_original_structure(base_path)

    of.organize_files(base_path, doc_path)
    of.organize_files(base_path)

    messagebox.showinfo("Done", "Files have been organized successfully.")
