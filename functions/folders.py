from functions import extensions as ext

CONTRACTS_FOLDER = "Contracts"
IDS_FOLDER = "IDs"
SIGNINOUT_FOLDER = "SignInOut"

## Create folder names
PRODUCTION_FOLDER = "1-Production"
POST_PRODUCTION_FOLDER = "2-Post_Production"
MASTERS_FOLDER = "3-Masters"

# Include the arrays with file name extensions inside the source folders.
SOURCE_FOLDERS = {
    "1-Source-Video": ext.VIDEO_EXTENSIONS,
    "2-Source-Audio": ext.AUDIO_EXTENSIONS,
    "3-Source-Images": ext.IMAGE_EXTENSIONS
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
