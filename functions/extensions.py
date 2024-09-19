# Load the library that allows to read JSON files
import json

# Load the JSON file that contains all accepted media file formats.
def load_file_formats(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
# Create a variable that represents the JSON file.
file_formats = load_file_formats('formats.json')

# Arrays that hold file name extensions.
VIDEO_EXTENSIONS = file_formats.get('video', [])
IMAGE_EXTENSIONS = file_formats.get('images', [])
AUDIO_EXTENSIONS = file_formats.get('audio', [])
DOCUMENT_EXTENSIONS = file_formats.get('documents', [])
