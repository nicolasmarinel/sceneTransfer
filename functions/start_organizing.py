from functions import organize_files as of, original_structure as ogs
# Importing the modules necessary for the graphic user interface.
from tkinter import messagebox

# The function called when the user presses the "Start" button.
def start_organizing(base_paths, doc_paths, multicam, imgFolders):

    # The following code was left in the code for future use.
    #site_code = site_code_entry.get()
    #print(site_code)

    # Eventually, multiple base paths and multiple doc paths will be supported.
    # This is why the code is written this way.
    for selection in base_paths:
        base_path = selection
    for selection in doc_paths:
        doc_path = selection

    # This logs the original structure of the files in the base path.
    ogs.log_original_structure(base_path)

    # This organizes the files in the document path.  The presence of the second argument
    # triggers different behavior in the function.
    of.organize_files(base_path, doc_path)
    # Here, we pass the second argument as None so the function reacts differently.
    of.organize_files(base_path, None, multicam, imgFolders)

    messagebox.showinfo("Done", "Files have been organized successfully.")
