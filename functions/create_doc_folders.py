import os

CONTRACTS_FOLDER = "Contracts"
IDS_FOLDER = "IDs"
SIGNINOUT_FOLDER = "SignInOut"

def create_doc_folders(base_path):
    created_folders = set()
    folders = [CONTRACTS_FOLDER, IDS_FOLDER, SIGNINOUT_FOLDER]
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        created_folders.add(folder_path)
        os.makedirs(folder_path, exist_ok=True)
    return created_folders
