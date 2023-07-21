# Website Crawler and Data Extractor

This is a Python script that implements a website crawler using Scrapy and extracts data from the crawled websites.
It also manages the created directories and creates a zip file containing the extracted data.

## Requirements
- Python 3.x
- Scrapy library (https://scrapy.org/)
- BeautifulSoup library (https://www.crummy.com/software/BeautifulSoup/)
- Requests library (https://docs.python-requests.org/en/latest/)

## Installation

Ensure you have Python 3.x installed on your system.
Install the required libraries using pip:
pip install scrapy beautifulsoup4 requests

You can install the dependencies using pip:

```shell
pip install -r requirements.txt
```

## Usage
1. Clone or download the script to your local machine.
2. Open a terminal or command prompt in the directory containing the script.
3. Run the script with the desired arguments:
```bash
python script.py [--ignore-web-crawler BOOL] [--ingnore-manage-directories BOOL] [--ignore-data-extractor BOOL]
                [--ignore-zip BOOL] [ ][--max-websites MAX_WEBSITES] [--start-urls START_URLS [START_URLS ...]]
                [--allowed-domains ALLOWED_DOMAINS [ALLOWED_DOMAINS ...]] [--delete-existing-directories BOOL]
```

## Example
Run the script
```bash
python script-web-crawler.py --delete-existing-directories True --max-websites 50
```


## Arguments:
- **--max-websites**: Optional. Maximum number of websites to crawl. If not provided, the script will crawl all accessible pages from the starting URLs.
- **--start-urls**: Optional. Space-separated list of starting URLs. If not provided, it will use the default starting URL ('https://myxalandri.gr').
- **--allowed-domains**: Optional. Space-separated list of allowed domains. If not provided, it will use the default allowed domain ('myxalandri.gr').

## Output
The script will crawl the websites, store the crawled URLs in 'crawled_urls.txt', and extract data from the crawled websites.
It will create three directories for each website in the current working directory:
- 'html_files': Contains the HTML documents of each crawled URL.
- 'txt_files': Contains extracted headlines and descriptions from JSON data of each URL.
- 'metadata_files': Contains metadata information (in JSON format) of each URL.
After the crawling and data extraction process, it will display the number of all pages, article pages, index pages, and the percentage of index pages.

## Zip File
The script will also create a zip file named "myxalandri.zip" that contains the extracted data from the crawled websites.
The zip file will include the three directories mentioned above.
Please note that the script will not remove any existing zip files or directories.

## Disclaimer
This script is provided as-is and may require modifications or updates based on your specific use case or the website's structure being crawled.
Use it responsibly and respect the website's terms of service when crawling and scraping data.
