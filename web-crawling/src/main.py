from website_processor import WebsiteProcessor
from website_directory_manager import WebsiteDirectoryManager
from website_data_extractor import MyXalandriDataExtractor, SportsNewsGreeceDataExtractor, MistikaKipouDataExtractor, TennisNewsDataExtractor
from website_data_analyzer import WebsiteDataAnalyzer
import argparse


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
    elif args.mode == 2:
        args.start_urls = ['https://www.mistikakipou.gr']
        args.allowed_domains = ['mistikakipou.gr']
    elif args.mode == 3:
        args.start_urls = ['https://tennisnews.gr']
        args.allowed_domains = ['tennisnews.gr']
    
    # TODO write a crawler for the http://ebooks.edu.gr/ website (that crawls all the sub domains of a specific book)
    
    if not args.ignore_web_crawler: 
        # Create a WebsiteProcessor instance and initiate the crawling and processing
        website_processor = WebsiteProcessor(args.max_websites, args.start_urls, args.allowed_domains)
        website_processor.crawl_and_process()

    if not args.ingnore_manage_directories:
        # Create a WebsiteDirectoryManager instance and manage the directories
        directory_manager = WebsiteDirectoryManager(crawled_urls_file = f'website_files/crawled_urls_{args.allowed_domains[0]}.txt', delete_existing_directories = args.delete_existing_directories, directory = "website_files/" + args.allowed_domains[0])
        dir_name =  directory_manager.create_directories()

    if not args.ignore_data_extractor:
        # Create a WebsiteDataExtractor instance and extract the data
        if args.mode == 0:
            data_extractor = MyXalandriDataExtractor(directory = "website_files/" + args.allowed_domains[0])
        elif args.mode == 1:
            data_extractor = SportsNewsGreeceDataExtractor(directory = "website_files/" + args.allowed_domains[0])
        elif args.mode == 2:
            data_extractor = MistikaKipouDataExtractor(directory = "website_files/" + args.allowed_domains[0])
        elif args.mode == 3:
            data_extractor = TennisNewsDataExtractor(directory = "website_files/" + args.allowed_domains[0])
        data_extractor.run(directory_manager.urls)

    if not args.ignore_zip:
        # Create a zip file
        directory_manager.create_zip_file(directory_name = ("website_files/" + dir_name), zip_file_name=args.allowed_domains[0])

    analytics = WebsiteDataAnalyzer(directory = "website_files/" + args.allowed_domains[0])
    sentences_dict = analytics.get_sentences_and_files()
    analytics.print_duplicates(sentences_dict)