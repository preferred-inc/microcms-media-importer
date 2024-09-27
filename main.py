import os
import mimetypes
import requests

# API / dir
API_ENDPOINT = ""
API_KEY = ""
DIRECTORY_PATH = ""

def upload_file(file_path):
    file_name = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type is None:
        mime_type = 'application/octet-stream'
    
    with open(file_path, 'rb') as fp:
        files = {
            'file': (file_name, fp, mime_type)
        }
        headers = {
            'X-MICROCMS-API-KEY': API_KEY
        }
        
        response = requests.post(API_ENDPOINT, headers=headers, files=files)
        
    if response.status_code == 201:
        print(f"Upload successful: {response.json()['url']}")
    else:
        print(f"Failed to upload {file_name}: {response.status_code} - {response.text}")

def upload_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            upload_file(file_path)

if __name__ == "__main__":
    if os.path.exists(DIRECTORY_PATH) and os.path.isdir(DIRECTORY_PATH):
        upload_directory(DIRECTORY_PATH)
    else:
        print(f"Directory {DIRECTORY_PATH} does not exist")
