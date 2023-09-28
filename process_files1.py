# with this logic
import redis

def process_file():
    r = redis.Redis(host='localhost', port=6379, db=0)
    file_path = r.rpop("file_queue")
    
    if file_path is None:
        return
    
    file_path = file_path.decode()
    
    try:
        # Replace with actual processing code
        processing_successful = True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        processing_successful = False

    if processing_successful:
        r.sadd("processed_files", file_path)




# example of some processing here. 



import os
import zipfile
import argparse
import py7zr
import rarfile
import gzip
import shutil
from collections import defaultdict

def extract_zip(file_path, extract_dir_path):
    with zipfile.ZipFile(file_path, 'r') as archive:
        archive.extractall(extract_dir_path)

def extract_7z(file_path, extract_dir_path):
    with py7zr.SevenZipFile(file_path, 'r') as archive:
        archive.extractall(extract_dir_path)

def extract_rar(file_path, extract_dir_path):
    with rarfile.RarFile(file_path, 'r') as archive:
        archive.extractall(extract_dir_path)

def extract_gz(file_path, extract_dir_path):
    with gzip.open(file_path, 'rb') as f_in:
        with open(extract_dir_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

archive_handlers = {
    '.zip': extract_zip,
    '.7z': extract_7z,
    '.rar': extract_rar,
    '.gz': extract_gz,
}

def unzip_files_in_dir(path, stats):
    for root, dirs, files in os.walk(path):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in archive_handlers:
                file_path = os.path.join(root, file)
                extract_dir_path = os.path.splitext(file_path)[0]
                if os.path.exists(extract_dir_path):
                    print(f"Directory {extract_dir_path} already exists. Conflict detected.")
                    continue
                try:
                    archive_handlers[ext](file_path, extract_dir_path)
                    stats[ext] += 1
                except Exception as e:
                    print(f"Failed to extract {file_path}: {e}")
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recursively unzip and unrar files in a directory.')
    parser.add_argument('path', help='Path of the target directory')
    args = parser.parse_args()

    stats = defaultdict(int)

    unzip_files_in_dir(args.path, stats)
    print("Extraction stats:")
    for key, value in stats.items():
        print(f"{key.upper()[1:]}: {value} files extracted")