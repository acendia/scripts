import argparse
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider


class AllSpider(scrapy.Spider):
    name = 'all'

    def __init__(self, max_crawled_websites=None, start_urls=None, allowed_domains=None):
        self.links = []
        self.max_crawled_websites = max_crawled_websites
        self.crawled_websites = 0
        self.file = open('crawled_urls.txt', 'w')

        if start_urls is not None:
            self.start_urls = start_urls
        if allowed_domains is not None:
            self.allowed_domains = allowed_domains

    def parse(self, response):
        if self.max_crawled_websites is not None and self.crawled_websites >= self.max_crawled_websites:
            self.file.close()
            raise CloseSpider('Maximum number of crawled websites reached')

        self.links.append(response.url)
        self.crawled_websites += 1

        url = response.url + '\n'
        self.file.write(url)

        # Print the number of crawled websites
        for href in response.css('a::attr(href)'):
            yield response.follow(href, self.parse)

    def closed(self, reason):
        # After the spider is closed, remove duplicates and save the crawled_urls list to the file.
        with open('crawled_urls.txt', 'r') as file:
            crawled_urls = file.readlines()

        crawled_urls = list(dict.fromkeys(crawled_urls))

        with open('crawled_urls.txt', 'w') as file:
            file.writelines(crawled_urls)


def main(max_crawled_websites=None, start_urls=None, allowed_domains=None):
    process = CrawlerProcess()
    process.crawl(
        AllSpider,
        max_crawled_websites=max_crawled_websites,
        start_urls=start_urls,
        allowed_domains=allowed_domains
    )
    process.start()

    # Read from the file crawled_urls.txt and print the total number of crawled websites.
    with open('crawled_urls.txt', 'r') as file:
        crawled_urls = file.readlines()
        print(f'\nTotal number of crawled websites: {len(crawled_urls)}')

    # Print the duplicated URLs.
    print('\nDuplicated URLs:')
    duplicates = set(url for url in crawled_urls if crawled_urls.count(url) > 1)
    for url in duplicates:
        print(url.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape websites and remove duplicates.')
    parser.add_argument('--max-websites', type=int, default=50, help='Maximum number of crawled websites.')
    parser.add_argument('--start-urls', nargs='+', default=['https://myxalandri.gr'], help='Space-separated list of starting URLs.')
    parser.add_argument('--allowed-domains', nargs='+', default=['myxalandri.gr'], help='Space-separated list of allowed domains.')
    args = parser.parse_args()

    main(args.max_websites, args.start_urls, args.allowed_domains)
