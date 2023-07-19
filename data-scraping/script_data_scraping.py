from bs4 import BeautifulSoup
import requests
import re
import json
import os
import shutil
import zipfile


def create_directories(site_maps_file, delete_existing_directories=False):
    """
    Create the directories for storing the HTML, TXT, and metadata files.
    """

    # Check if the file exists
    if not os.path.exists(site_maps_file):
        print('File does not exist')
        return

    # Read the file and save each URL from each line to a list
    with open(site_maps_file, 'r') as f:
        urls = f.readlines()

    directory_list = []

    for url in urls:
        # Extract the domain name and top-level domain (TLD) from the URL
        domain_dot_tld = re.search(r'(?<=https://)(.*?)(?=/)', url).group(0)

        # Check if the directory exists (directory name contains the domain name and TLD)
        if not os.path.exists(domain_dot_tld):
            print(f'Creating new directory {domain_dot_tld}')
            os.makedirs(domain_dot_tld)
        elif delete_existing_directories:
            print(f'Directory {domain_dot_tld} already exists. Deleting it and creating a new one')
            # Delete the directory and create a new one
            shutil.rmtree(domain_dot_tld)
            os.makedirs(domain_dot_tld)
        else:
            print(f'Directory {domain_dot_tld} already exists')

        directory_list.append(domain_dot_tld)

        # Create 3 directories under the domain_dot_tld directory: html_files, txt_files, metadata_files
        html_files_dir = os.path.join(domain_dot_tld, 'html_files')
        txt_files_dir = os.path.join(domain_dot_tld, 'txt_files')
        metadata_files_dir = os.path.join(domain_dot_tld, 'metadata_files')

        # Check if the directories exist
        for directory in [html_files_dir, txt_files_dir, metadata_files_dir]:
            if not os.path.exists(directory):
                print(f'Creating new directory {directory}')
                os.makedirs(directory)
            else:
                print(f'Directory {directory} already exists')

    return directory_list, urls


def is_index_page(soup, tag):
    """
    Check if the URL is an index page.
    """
    meta_tags = soup.find_all('meta', attrs={'name': 'author'})
    if meta_tags:
        print(f'Website: {tag.text}')
        print('--' * 80)
        return False
    else:
        print(f'Website: {tag.text}')
        print("This is an index page. No meta tags with name author")
        print('--' * 80)
        return True


def extract_html(html_document, domain_dot_tld, idx_file):
    """
    Extract the HTML document from the URL
    """
    html_file_path = os.path.join(domain_dot_tld, "html_files", f"{idx_file}.html")
    with open(html_file_path, 'w') as f:
        f.write(html_document.text)


def extract_headline_and_description(soup, domain_dot_tld, idx_file):
    """
    Extract the headline and description from the JSON data
    """
    script_tags = soup.find_all('script', attrs={'data-type': 'gsd'})

    for script_tag in script_tags:
        json_data = script_tag.string.strip()
        data = json.loads(json_data)
        headline = data.get('headline')
        description = data.get('description')

        if headline is not None and description is not None:
            txt_file_path = os.path.join(domain_dot_tld, "txt_files", f"{idx_file}.txt")
            with open(txt_file_path, 'w') as f:
                f.write('Title:\n' + headline + '\n')
                f.write('Description:\n' + description + '\n')


def extract_metadata(soup, domain_dot_tld, idx_file):
    """
    Extract the metadata from the HTML document
    """
    meta_tags = soup.find_all('meta')

    metadata = {}
    for meta_tag in meta_tags:
        name = meta_tag.get('name')
        content = meta_tag.get('content')
        if name and content:
            metadata[name] = content

    meta_file_path = os.path.join(domain_dot_tld, "metadata_files", f"{idx_file}.meta")
    with open(meta_file_path, 'w') as f:
        f.write(json.dumps(metadata, indent=4, ensure_ascii=False))


def create_zip_file(directory_list, zip_file_name="mydirectories.zip"):
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for directory_name in directory_list:
            directory_path = os.path.abspath(directory_name)
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, directory_path))

    print("Zip file created successfully:", zip_file_name)


def main():
    site_maps_file = 'sitemaps.txt'
    delete_existing_directories = True
    directory_list, urls = create_directories(site_maps_file, delete_existing_directories)

    idx_article_page = 0
    idx_index_page = 0

    # Remove the trailing newline character
    urls[0] = urls[0].rstrip()

    xml_document = requests.get(urls[0])
    soup = BeautifulSoup(xml_document.text, 'html.parser')
    loc_tags = soup.find_all('loc')

    for tag in loc_tags[:50]:
        html_document = requests.get(tag.text)
        soup = BeautifulSoup(html_document.text, 'html.parser')

        # Skip front page and index pages
        if tag.text.split('/')[-1] == '':
            continue

        if is_index_page(soup, tag):
            idx_index_page += 1
            continue

        domain_dot_tld = re.search(r'(?<=https://)(.*?)(?=/)', urls[0]).group(0)
        print(domain_dot_tld)

        # Extracting phase
        extract_html(html_document, domain_dot_tld, idx_article_page)
        extract_headline_and_description(soup, domain_dot_tld, idx_article_page)
        extract_metadata(soup, domain_dot_tld, idx_article_page)

        idx_article_page += 1

    # Show information about the files extracted
    print('###' * 30)
    print(f'Number of all pages: {idx_article_page + idx_index_page}')
    print(f'Number of article pages: {idx_article_page}')
    print(f'Number of index pages: {idx_index_page}')
    print(f'Percentage of index pages: {round(idx_index_page / idx_article_page * 100, 2)}%')

    create_zip_file(directory_list)


if __name__ == '__main__':
    main()
