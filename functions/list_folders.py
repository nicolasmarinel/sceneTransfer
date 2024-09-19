import os

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
