import requests
from bs4 import BeautifulSoup
import json
import re


class WebsiteDataExtractor():
    def __init__(self):
        pass

    def is_index_page(self, soup, tag):
        """
        Check if the URL is an index page.
        """
        # get all meta tags with name author
        meta_tags = soup.find_all('meta', attrs={'name': 'author'})
        if meta_tags:
            print(f'Website: {tag}')
            # print(meta_tags)
            print('--' * 60)
            return 0 # return 0 if it is not an index page
        else:
            print(f'Website: {tag}')
            print("This is an index page. No meta tags with name author")
            print('--' * 60)
            return 1 # return 1 if it is an index page


    def extract_html(self, html_document, dir_name, idx_file):
        """
        Extract the HTML document from the URL
        """

        # Write the HTML document to a .html file
        with open(dir_name + "/html_files/" +  str(idx_file) + '.html', 'w') as f:
            f.write(html_document.text)
            f.close()    

    def extract_headline_and_description(self, soup, dir_name, idx_file):
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
                with open(dir_name + "/txt_files/" +  str(idx_file) + '.txt', 'w') as f:
                    f.write('Title:'+ '\n' + headline + '\n')
                    f.write('Description:' + '\n' + description + '\n')
                    f.close()

    def extract_metadata(self, soup, dir_name, idx_file):
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
        meta_file = dir_name + "/metadata_files/" +  str(idx_file) + '.meta'
        with open(meta_file, 'w') as f:
            f.write(json.dumps(metadata, indent=4, ensure_ascii=False))



    def run(self, urls):
        """
        Run the data extraction process
        """
        idx_article_page = 0
        idx_index_page = 0

        # Loop over each tag and extract the data
        # for tag in loc_tags:
        for tag in urls[1:]:
            # Retrieve the HTML document using the get() method of the requests module
            html_document = requests.get(tag)

            # Create a BeautifulSoup object for parsing the HTML document
            soup = BeautifulSoup(html_document.text, 'html.parser')

            # if url is front page, skip
            if tag.split('/')[-1] == '': 
                continue

            # if url is index page, skip
            if self.is_index_page(soup, tag):
                idx_index_page += 1
                continue
            
            # Extract the domain name and TLD from the URL
            dir_name =  re.search(r"(?<=://)(.*?)(?=\.gr)", urls[0]).group(0)

            # Extracting phase
            self.extract_html(html_document, dir_name, idx_article_page)

            self.extract_headline_and_description(soup, dir_name, idx_article_page)

            self.extract_metadata(soup, dir_name, idx_article_page)

            idx_article_page += 1

        # Show information about the files extracted
        print('##' * 60)
        print(f'Number of all pages: {idx_article_page + idx_index_page}')
        print(f'Number of article pages: {idx_article_page}')
        print(f'Number of index pages: {idx_index_page}')
        print(f'Percentage of index pages: {round(idx_index_page/(idx_article_page + idx_index_page)*100, 2)}%')
        print(f'Percentage of article pages: {round(idx_article_page/(idx_article_page + idx_index_page)*100, 2)}%')
