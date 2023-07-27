from website_crawler import WebsiteCrawler
from scrapy.crawler import CrawlerProcess
import os
import scrapy


class WebsiteProcessor:
    """
    This class is responsible for initiating the crawling process and processing the crawled URLs.
    """
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

    def process_crawled_urls(self, ):
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
