import argparse
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider

from bs4 import BeautifulSoup
import requests
import re
import json
import os
import shutil
import zipfile
import logging
from collections import defaultdict
import numpy as np

# Disable log messages
# logging.getLogger('scrapy').propagate = False
# logging.getLogger('scrapy').setLevel(logging.WARNING)


class WebsiteCrawler(scrapy.Spider):
    name = 'website_crawler'

    def __init__(self, max_crawled_websites=None, start_urls=None, allowed_domains=None):
        super().__init__()
        self.links = []
        self.max_crawled_websites = max_crawled_websites
        self.crawled_websites = 0
        self.file = open(f'crawled_urls_{allowed_domains[0]}.txt', 'w')

        if start_urls is not None:
            self.start_urls = start_urls
        if allowed_domains is not None:
            self.allowed_domains = allowed_domains

    def parse(self, response):
        # Check if the maximum number of crawled websites has been reached
        if self.max_crawled_websites is not None and self.crawled_websites >= self.max_crawled_websites:
            self.file.close()
            raise CloseSpider('Maximum number of crawled websites reached')

        # Track the crawled website URLs
        self.links.append(response.url)
        self.crawled_websites += 1

        # Write the current URL to the file
        url = response.url + '\n'
        self.file.write(url)

        # Follow the URLs found in the current page
        for href in response.css('a::attr(href)'):
            yield response.follow(href, self.parse)

    def closed(self, reason):
        # After the spider is closed, remove duplicates and save the crawled_urls list to the file.
        with open(f'crawled_urls_{self.allowed_domains[0]}.txt', 'r') as file:
            crawled_urls = file.readlines()

        # Remove duplicates using a dictionary and save the deduplicated URLs
        crawled_urls = list(dict.fromkeys(crawled_urls))
        with open(f'crawled_urls_{self.allowed_domains[0]}.txt', 'w') as file:
            file.writelines(crawled_urls)


class WebsiteProcessor:
    def __init__(self, max_crawled_websites=None, start_urls=None, allowed_domains=None):
        self.max_crawled_websites = max_crawled_websites
        self.start_urls = start_urls
        self.allowed_domains = allowed_domains

    def crawl_and_process(self):
        # Start the crawling process using Scrapy's CrawlerProcess
        process = CrawlerProcess()
        process.crawl(
            WebsiteCrawler,
            max_crawled_websites=self.max_crawled_websites,
            start_urls=self.start_urls,
            allowed_domains=self.allowed_domains
        )
        process.start()

        # Call the function to process crawled URLs after the spider is closed.
        self.process_crawled_urls()

    def process_crawled_urls(self,):
        # Read from the file crawled_urls.txt and print the total number of crawled websites.
        with open(f'crawled_urls_{self.allowed_domains[0]}.txt', 'r') as file:
            crawled_urls = file.readlines()
            print(f'\nTotal number of crawled websites: {len(crawled_urls)}')

        # Print the duplicated URLs.
        print('\nDuplicated URLs:')
        duplicates = set(url for url in crawled_urls if crawled_urls.count(url) > 1)
        for url in duplicates:
            print(url.strip())

        
        # Remove duplicates using a dictionary and save the deduplicated URLs
        crawled_urls = list(dict.fromkeys(crawled_urls))
        with open(f'crawled_urls_{self.allowed_domains[0]}.txt', 'w') as file:
            file.writelines(crawled_urls)


class WebsiteDirectoryManager:
    def __init__(self, crawled_urls_file=None, delete_existing_directories=False, directory=None):
        self.crawled_urls_file = crawled_urls_file
        self.delete_existing_directories = delete_existing_directories
        self.url = None
        self.urls = []
        self.directory = directory

    def read_urls_from_file(self):
        if os.path.exists(self.crawled_urls_file):
            with open(self.crawled_urls_file, 'r') as f:
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
        # dir_name = re.search(r"(?<=://)(.*?)(?=\.gr)", self.url).group(0)
        dir_name = self.directory
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
    def create_zip_file(self, directory_name, zip_file_name=None):
        zip_file_name = zip_file_name + ".zip"
        with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
            directory_path = os.path.abspath(directory_name)
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, directory_path))

        print("Zip file created successfully:", zip_file_name)

    
class WebsiteDataExtractor():
    def __init__(self, directory=None):
        self.directory = directory

    def is_index_page(self, soup, tag):
        """
        Check if the URL is an index page.
        """
        # get all meta tags with name author
        meta_tags = soup.find_all('meta', attrs={'name': 'author'})
        if meta_tags:
            print('--' * 60)
            print(f'Website: {tag}')
            # return 0 if it is not an index page
            return 0 
        else:
            print('--' * 60)
            print(f'Website: {tag}')
            print("This is an index page. No meta tags with name author")
            # return 1 if it is an index page
            return 1 
        


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
            # dir_name =  re.search(r"(?<=://)(.*?)(?=\.gr)", urls[0]).group(0)
            dir_name = self.directory
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


class MyXalandriDataExtractor(WebsiteDataExtractor):
    def __init__(self, directory=None):
        self.directory = directory

    def is_index_page(self, soup, tag):
        """
        Check if the URL is an index page.
        """
        # get all meta tags with name author
        meta_tags = soup.find_all('meta', attrs={'name': 'author'})
        if meta_tags:
            print('--' * 60)
            print(f'Website: {tag}')
            # return 0 if it is not an index page
            return 0 
        else:
            print('--' * 60)
            print(f'Website: {tag}')
            print("This is an index page. No meta tags with name author")
            # return 1 if it is an index page
            return 1 
    
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
    

class SportsNewsGreeceDataExtractor(WebsiteDataExtractor):
    def __init__(self, directory=None):
        self.directory = directory

    def is_index_page(self, soup, tag):
        """
        Check if the URL is an index page.
        """
        # get all meta tags with name author
        meta_tags = script_tag = soup.find('script', type='application/ld+json')
        num_meta_tags = len(soup.find_all('script', type='application/ld+json'))

        if meta_tags and num_meta_tags == 2:
            print(f'Website: {tag}')
            # print(meta_tags)
            print('--' * 60)
            return 0 # return 0 if it is not an index page
        else:
            print(f'Website: {tag}')
            print("This is an index (or useless) page.")
            print('--' * 60)
            return 1 # return 1 if it is an index page

    def extract_headline_and_description(self, soup, dir_name, idx_file):
        """
        Extract the headline and description
        """
        # Find the title tag and extract the text
        title = soup.find('title').get_text(strip=True)
        
        ### Solution - 1 (Contains part of the description information, but it is separated by paragraphs)
        # Find the div containing the post content
        content_tag = soup.find('div', class_='post-body post-content')
        # Find the paragraphs inside the div
        paragraphs = content_tag.find_all('p')
        # Combine paragraphs and separate them with a new line
        description = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        
        ### Solution - 2 (Contains all the description information, but it is not separated by paragraphs)     
        # Find the div containing the post content
        # description = soup.find('div', class_='post-body post-content').get_text(strip=True)

        # Write the headline and description to a .txt file
        with open(dir_name + "/txt_files/" + str(idx_file) + '.txt', 'w') as f:
            f.write('Title:\n' + title + '\n')
            f.write('Description:\n' + description + '\n')
            f.close()

    def extract_metadata(self, soup, dir_name, idx_file):
        """
        Extract the metadata from the HTML document
        """

        # Find all <meta> tags
        meta_tags = soup.find_all('meta')

        json_script = soup.find_all('script', type='application/ld+json')
        data = json.loads(json_script[0].string)
        
        url_id = data["mainEntityOfPage"]["@id"]
        headline = data["headline"]
        date_published = data["datePublished"]
        date_modified = data["dateModified"]
        author = data["author"]["name"]

        print("URL:", url_id)
        print("Headline:", headline)
        print("Date Published:", date_published)
        print("Date Modified:", date_modified)
        print("Author:", author)

        
        data_topic = json.loads(json_script[1].string)
        topic = [item["item"]["name"] for item in data_topic["itemListElement"]]
        print(topic)

        extracted_data = {
            "URL": url_id,
            "Topic": topic[:-1],
            "Headline": headline,
            "Date Published": date_published,
            "Date Modified": date_modified,
            "Author": author
        }


        # # Extract the desired metadata from each meta tag
        # metadata = {}
        # for meta_tag in meta_tags:
        #     name = meta_tag.get('name')
        #     content = meta_tag.get('content')
        #     if name and content:
        #         metadata[name] = content

        # Write the metadata to a .meta file in JSON format
        meta_file = dir_name + "/metadata_files/" +  str(idx_file) + '.meta'
        with open(meta_file, 'w') as f:
            f.write(json.dumps(extracted_data, indent=4, ensure_ascii=False))


class WebsiteDataAnalyzer():
    def __init__(self, directory = None):
        self.directory = directory

    def get_sentences_from_text(self, text):
        # Split text into sentences using a regular expression.
        sentences = re.split(r'[.!?]', text)
        # Remove any leading/trailing whitespaces from sentences.
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        return sentences

    def get_sentences_and_files(self,):
        sentences_dict = defaultdict(list)
        for filename in os.listdir(f'{self.directory}/txt_files/'):
            # print('--', filename)
            if filename.endswith('.txt'):
                with open(f'{self.directory}/txt_files/'+filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Extract the description section using regex.
                    description_match = re.search(r'Description:(.+)', content, re.DOTALL)
                    if description_match:
                        description_text = description_match.group(1)
                        sentences = self.get_sentences_from_text(description_text)
                        for sentence in sentences:
                            sentences_dict[sentence].append(filename)
        return sentences_dict

    def print_duplicates(self, sentences_dict):
        for sentence, files in sentences_dict.items():
            # if length of sentence is greater than 10 characters:
            if len(sentence) > 50:
                if len(np.unique(files)) > 1 and len(files) > 1:
                    print(f"Sentence: {sentence}")
                    print("Found in files:", ", ".join(np.unique(files)))
                    print()


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Scrape websites and remove duplicates.')
    parser.add_argument('--ignore-web-crawler', type=bool, default=False, help='Ignore the web crawler and process the crawled URLs.')
    parser.add_argument('--ingnore-manage-directories', type=bool, default=False, help='Ignore the directory manager and process the crawled URLs.')
    parser.add_argument('--ignore-data-extractor', type=bool, default=False, help='Ignore the data extractor and process the crawled URLs.')
    parser.add_argument('--ignore-zip', type=bool, default=False, help='Ignore the zip file creation.')
    

    parser.add_argument('--max-websites', type=int, default=None, help='Maximum number of crawled websites.')
    parser.add_argument('--start-urls', nargs='+', default=['https://myxalandri.gr'], help='Space-separated list of starting URLs.')
    parser.add_argument('--allowed-domains', nargs='+', default=['myxalandri.gr'], help='Space-separated list of allowed domains.')
    parser.add_argument('--delete-existing-directories', type=bool, default=False, help='Delete existing directories.')

    parser.add_argument('--mode', type=int, default=0, help='Website to crawl. 0: myxalandri.gr, 1: sportsnews.gr')
    args = parser.parse_args()

    if args.mode == 1: 
        args.start_urls = ['https://www.sportsnewsgreece.gr']
        args.allowed_domains = ['sportsnewsgreece.gr']

    if not args.ignore_web_crawler: 
        # Create a WebsiteProcessor instance and initiate the crawling and processing
        website_processor = WebsiteProcessor(args.max_websites, args.start_urls, args.allowed_domains)
        website_processor.crawl_and_process()

    if not args.ingnore_manage_directories:
        # Create a WebsiteDirectoryManager instance and manage the directories
        directory_manager = WebsiteDirectoryManager(crawled_urls_file = f'crawled_urls_{args.allowed_domains[0]}.txt', delete_existing_directories = args.delete_existing_directories, directory = args.allowed_domains[0])
        dir_name =  directory_manager.create_directories()

    if not args.ignore_data_extractor:
        # Create a WebsiteDataExtractor instance and extract the data
        if args.mode == 0:
            data_extractor = MyXalandriDataExtractor(directory = args.allowed_domains[0])
        else:
            data_extractor = SportsNewsGreeceDataExtractor(directory = args.allowed_domains[0])
        
        data_extractor.run(directory_manager.urls)

    if not args.ignore_zip:
        # Create a zip file
        directory_manager.create_zip_file(directory_name = dir_name, zip_file_name=args.allowed_domains[0])

    analytics = WebsiteDataAnalyzer(directory = args.allowed_domains[0])
    sentences_dict = analytics.get_sentences_and_files()
    analytics.print_duplicates(sentences_dict)

