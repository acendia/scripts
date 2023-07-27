import requests
from bs4 import BeautifulSoup
import json
import re
import bs4

class WebsiteDataExtractor():
    """
    This class is responsible for extracting the data from the crawled websites.
    """
    
    def __init__(self, directory=None):
        self.directory = directory

    def is_index_page(self, soup, tag):
        """
        Check if the URL is an index page.
        """
        raise NotImplementedError("is_index_page method must be implemented in child classes.")


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
        Extract the headline and description from the HTML document
        """
        raise NotImplementedError("extract_headline_and_description method must be implemented in child classes.")

    def extract_metadata(self, soup, dir_name, idx_file):
        """
        Extract the metadata from the HTML document
        """
        raise NotImplementedError("extract_metadata method must be implemented in child classes.")



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

            # TODO: bad code - fix it
            # # if url is front page, skip
            # if tag.split('/')[-1] == '': 
            #     continue

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


##############################################################################################################


class MyXalandriDataExtractor(WebsiteDataExtractor):
    """
    This class is responsible for extracting the data from the crawled websites from myxalandri.gr.
    """

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


##############################################################################################################


class SportsNewsGreeceDataExtractor(WebsiteDataExtractor):
    """
    This class is responsible for extracting the data from the crawled websites from sportsnews.gr.
    """

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

        # Write the metadata to a .meta file in JSON format
        meta_file = dir_name + "/metadata_files/" +  str(idx_file) + '.meta'
        with open(meta_file, 'w') as f:
            f.write(json.dumps(extracted_data, indent=4, ensure_ascii=False))


##############################################################################################################


class MistikaKipouDataExtractor(WebsiteDataExtractor):
    """
    This class is responsible for extracting the data from the crawled websites from mistikakipou.gr.
    """

    def is_index_page(self, soup, tag):
        """
        Check if the URL is an index page.
        """
        # get meta tags
        meta_tags = soup.find_all('meta')
        # get meta_tag with name "keywords"
        meta_tag = soup.find('meta', attrs={'name': 'keywords'})
        # if it exists return 0 else return 1
        if meta_tag:
            print('--' * 60)
            print(f'Website: {tag}')
            return 0
        else:
            print('--' * 60)
            print(f'Website: {tag}')
            print("This is an index page. No meta tags with name keywords")
            return 1


    # Function to get the text from a tag while ignoring anchor tags
    def get_text_from_tag(self, tag):
        if isinstance(tag, bs4.NavigableString):
            return tag.strip()
        elif tag.name == 'a':  # Ignore anchor tags
            return ' ' + tag.get_text(strip=True).strip() + ' '
        else:
            return ''.join(self.get_text_from_tag(child) for child in tag.contents)


    def extract_headline_and_description(self, soup, dir_name, idx_file):
        """
        Extract the headline and description
        """
        soup = soup.find('div', class_='entry-content')
        title = soup.find('h1', class_='entry-title').get_text(strip=True)
        
        paragraphs = soup.find_all(['h4', 'h3', 'h2', 'p', 'li'])

        # Write the headline and description to a .txt file
        with open(dir_name + "/txt_files/" + str(idx_file) + '.txt', 'w') as f:
            f.write('Title:\n' + title + '\n')
            
            # Write the 'Description' label only once at the start
            f.write('Description:\n')
            
            # Separate paragraphs with newlines and write them to the file
            for paragraph in paragraphs:
                paragraph_text = self.get_text_from_tag(paragraph)
                if paragraph.name == 'li':
                    paragraph_text = '* ' + paragraph_text.strip()
                
                if "A post shared by Τα Μυστικά του Κήπου (@mistikakipou)" in paragraph_text:
                    continue
                
                f.write(paragraph_text + '\n\n')


    def extract_metadata(self, soup, dir_name, idx_file):
        """
        Extract the metadata from the HTML document
        """

        # find all <meta> tags
        title = soup.find('meta', attrs={'property': 'og:title'})
        url = soup.find('meta', attrs={'property': 'og:url'})
        published_time = soup.find('meta', attrs={'property': 'article:published_time'})
        modified_time = soup.find('meta', attrs={'property': 'article:modified_time'})
    
        extracted_data = {
            "URL": url["content"],
            "Title": title["content"],
            "Published Time": published_time["content"] if published_time else None,
            "Modified Time": modified_time["content"] if modified_time else None
        }
        
        # Write the metadata to a .meta file in JSON format
        meta_file = dir_name + "/metadata_files/" +  str(idx_file) + '.meta'
        with open(meta_file, 'w') as f:
            f.write(json.dumps(extracted_data, indent=4, ensure_ascii=False))
