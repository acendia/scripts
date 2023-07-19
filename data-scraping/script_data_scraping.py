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

        # create 3 directories under the domain_dot_tld directory: html_files, txt_files, metadata_files
        html_files = os.path.join(domain_dot_tld, 'html_files')
        txt_files = os.path.join(domain_dot_tld, 'txt_files')
        metadata_files = os.path.join(domain_dot_tld, 'metadata_files')

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
    
    return directory_list, urls

### STAGE 2: Functions that extract the data from the HTML files ###

def is_index_page(soup, tag):
    """
    Check if the URL is an index page.
    """

    # get all meta tags with name author
    meta_tags = soup.find_all('meta', attrs={'name': 'author'})
    if meta_tags:
        print(f'Website: {tag.text}')
        # print(meta_tags)
        print('--' * 80)
        return 0 # return 0 if it is not an index page
    else:
        print(f'Website: {tag.text}')
        print("This is an index page. No meta tags with name author")
        print('--' * 80)
        return 1 # return 1 if it is an index page


def extract_html(html_document, domain_dot_tld, idx_file):
    """
    Extract the HTML document from the URL
    """

    # Write the HTML document to a .html file
    with open(domain_dot_tld + "/html_files/" +  str(idx_file) + '.html', 'w') as f:
        f.write(html_document.text)
        f.close()    


def extract_headline_and_description(soup, domain_dot_tld, idx_file):
    """
    Extract the headline and description from the JSON data
    """
    
    script_tags = soup.find_all('script', attrs={'data-type': 'gsd'})

    # Extract the headline and description from each script tag
    for script_tag in script_tags:
        # Extract the JSON data
        json_data = script_tag.string.strip()

        # Parse the JSON data
        data = json.loads(json_data)

        # Extract the headline and description using the get() method
        headline = data.get('headline')
        description = data.get('description')

        # Print the extracted values
        if headline is not None and description is not None:
            with open(domain_dot_tld + "/txt_files/" +  str(idx_file) + '.txt', 'w') as f:
                f.write('Title:'+ '\n' + headline + '\n')
                f.write('Description:' + '\n' + description + '\n')
                f.close()


def extract_metadata(soup, domain_dot_tld, idx_file):
    """
    Extract the metadata from the HTML document
    """

    # Find all <meta> tags
    meta_tags = soup.find_all('meta')

    # Extract the desired metadata from each meta tag
    metadata = {}
    for meta_tag in meta_tags:
        name = meta_tag.get('name')
        content = meta_tag.get('content')
        if name and content:
            metadata[name] = content

    # Write the metadata to a .meta file in JSON format
    meta_file = domain_dot_tld + "/metadata_files/" +  str(idx_file) + '.meta'
    with open(meta_file, 'w') as f:
        f.write(json.dumps(metadata, indent=4, ensure_ascii=False))




def create_zip_file(directory_list, zip_file_name="mydirectories.zip"):
    # Create a new zip file and open it in write mode
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Add each directory and its contents to the zip file
        for directory_name in directory_list:
            # Get the absolute path of the directory
            directory_path = os.path.abspath(directory_name)
            
            # Iterate over all the files and folders in the directory
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    # Get the absolute path of each file
                    file_path = os.path.join(root, file)
                    
                    # Add the file to the zip file using the relative path
                    zip_file.write(file_path, os.path.relpath(file_path, directory_path))

    print("Zip file created successfully: ", zip_file_name)



if __name__ == '__main__':

    ### Stage 1 ###

    site_maps_file = 'sitemaps.txt'
    delete_existing_directories = True
    directory_list, xml = create_directories(site_maps_file, delete_existing_directories)


    ### Stage 2 ###

    idx_article_page = 0
    idx_index_page = 0

    # Remove the trailing newline character
    xml[0] = xml[0].rstrip()

    xml_document = requests.get(xml[0])
    # Parse the XML document
    soup = BeautifulSoup(xml_document.text, 'html.parser')
    # Find all the <loc> tags
    loc_tags = soup.find_all('loc')


    # Loop over each tag and extract the data
    for tag in loc_tags[:50]:
        # Retrieve the HTML document using the get() method of the requests module
        html_document = requests.get(tag.text)

        # Create a BeautifulSoup object for parsing the HTML document
        soup = BeautifulSoup(html_document.text, 'html.parser')

        # if url is front page, skip
        if tag.text.split('/')[-1] == '': 
            continue

        # if url is index page, skip
        if is_index_page(soup, tag):
            idx_index_page += 1
            continue
        
        # Extract the domain name and TLD from the URL
        domain_dot_tld = re.search(r'(?<=https://)(.*?)(?=/)', xml[0]).group(0)
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
    print(f'Percentage of index pages: {round(idx_index_page/idx_article_page*100, 2)}%')

    ## Stage 3 ###
    create_zip_file(directory_list)
