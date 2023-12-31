import scrapy
from scrapy.exceptions import CloseSpider
import os 

class WebsiteCrawler(scrapy.Spider):
    """
    This class is responsible for crawling the websites.
    """
    name = 'website_crawler'

    def __init__(self, max_crawled_websites=None, start_urls=None, allowed_domains=None):
        super().__init__()
        self.links = []
        self.max_crawled_websites = max_crawled_websites
        self.crawled_websites = 0
        
        # if directory website_files does not exist, create it:
        if not os.path.exists('website_files'):
            os.makedirs('website_files')
    
        self.file = open(f'website_files/crawled_urls_{allowed_domains[0]}.txt', 'w')

        if start_urls is not None:
            self.start_urls = start_urls
        if allowed_domains is not None:
            self.allowed_domains = allowed_domains

    def parse(self, response):
        """
        This method is responsible for parsing the response.
        """
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
        """
        This method is called when the spider is closed.
        """
        # After the spider is closed, remove duplicates and save the crawled_urls list to the file.
        with open(f'website_files/crawled_urls_{self.allowed_domains[0]}.txt', 'r') as file:
            crawled_urls = file.readlines()

        # Remove duplicates using a dictionary and save the deduplicated URLs
        crawled_urls = list(dict.fromkeys(crawled_urls))

        with open(f'website_files/crawled_urls_{self.allowed_domains[0]}.txt', 'w') as file:
            file.writelines(crawled_urls)
