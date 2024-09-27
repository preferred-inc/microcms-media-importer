import os
import mimetypes
import requests
import csv
from datetime import datetime
from time import sleep
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = os.environ['API_ENDPOINT']
API_KEY = os.environ['API_KEY']
DIRECTORY_PATH = "./files/"
CSV_FILE_PATH = "./uploaded_files.csv"

uploaded_files = []

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
        upload_url = response.json()['url']
        print(f"Upload successful: {upload_url}")
        uploaded_files.append((file_name, upload_url))
    else:
        print(f"Failed to upload {file_name}: {response.status_code} - {response.text}")

def upload_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            upload_file(file_path)
            sleep(0.5)

def save_uploaded_files_to_csv(csv_file_path, data):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File Name", "URL"])
        writer.writerows(data)

if __name__ == "__main__":
    if os.path.exists(DIRECTORY_PATH) and os.path.isdir(DIRECTORY_PATH):
        upload_directory(DIRECTORY_PATH)
        save_uploaded_files_to_csv(CSV_FILE_PATH, uploaded_files)
        print(f"Uploaded file information saved to {CSV_FILE_PATH}")
    else:
        print(f"Directory {DIRECTORY_PATH} does not exist")