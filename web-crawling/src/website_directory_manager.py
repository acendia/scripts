import os
import re
import shutil
import zipfile

class WebsiteDirectoryManager:
    def __init__(self, site_maps_file='crawled_urls.txt', delete_existing_directories=False):
        self.site_maps_file = site_maps_file
        self.delete_existing_directories = delete_existing_directories
        self.url = None
        self.urls = []

    def read_urls_from_file(self):
        if os.path.exists(self.site_maps_file):
            with open(self.site_maps_file, 'r') as f:
                self.urls = f.readlines()
                self.urls = [url.strip() for url in self.urls]
                print(f'Number of urls: {len(self.urls)}')
                print(f'First url: {self.urls[0]}')
                self.url = self.urls[0]
        else:
            print('File does not exist')
            raise FileNotFoundError('File does not exist')

    def create_directories(self):
        self.read_urls_from_file()
        if self.url is None:
            return

        # Extract the domain name and top-level domain (TLD) from the URL
        dir_name = re.search(r"(?<=://)(.*?)(?=\.gr)", self.url).group(0)

        # Check if the directory exists (directory name contains the domain name and TLD)
        if not os.path.exists(dir_name):
            print(f'Creating new directory {dir_name}')
            os.makedirs(dir_name)
        elif self.delete_existing_directories:
            print(f'Directory {dir_name} already exists. Deleting it and creating a new one')
            # Delete the directory and create a new one
            shutil.rmtree(dir_name)
            os.makedirs(dir_name)
        else:
            print(f'Directory {dir_name} already exists')

        # create 3 directories under the dir_name directory: html_files, txt_files, metadata_files
        html_files = os.path.join(dir_name, 'html_files')
        txt_files = os.path.join(dir_name, 'txt_files')
        metadata_files = os.path.join(dir_name, 'metadata_files')

        # Check if the directories exist
        if not os.path.exists(html_files):
            print(f'Creating new directory {html_files}')
            os.makedirs(html_files)
        else:
            print(f'Directory {html_files} already exists')

        if not os.path.exists(txt_files):
            print(f'Creating new directory {txt_files}')
            os.makedirs(txt_files)
        else:
            print(f'Directory {txt_files} already exists')

        if not os.path.exists(metadata_files):
            print(f'Creating new directory {metadata_files}')
            os.makedirs(metadata_files)
        else:
            print(f'Directory {metadata_files} already exists')

        print('--' * 60)
        return dir_name
    
    # zip the directories
    def create_zip_file(self, directory_name, zip_file_name="myxalandri"):
        zip_file_name = zip_file_name + ".zip"
        with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
            directory_path = os.path.abspath(directory_name)
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, directory_path))

        print("Zip file created successfully:", zip_file_name)
