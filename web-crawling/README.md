# Web Crawler Script (script-web-crawler.py)

This is a Python script that utilizes Scrapy to crawl websites, starting from a given URL and domain, and saves the crawled URLs to a file named `crawled_urls.txt`. Additionally, it removes any duplicate URLs from the list of crawled websites.

## Requirements

- Python 3.x
- Scrapy library


You can install the dependencies using pip:
```bash
pip install -r requirements.txt
```
## Installation

Make sure you have Python 3.x installed. To install the required libraries, run the following command:

```bash
pip install scrapy
```

## Usage

```bash
python script-web-crawler.py [--max-websites MAX_WEBSITES]
```


## Arguments

- `--max-websites`: (optional) The maximum number of websites to be crawled. If not specified, the script will crawl all reachable URLs from the starting URL.

## How it works

1. The script starts crawling from the specified starting URL and domain.
2. The crawled URLs are saved to `crawled_urls.txt`.
3. After the spider is closed, any duplicate URLs in `crawled_urls.txt` are removed, ensuring a unique list of crawled websites.
4. The total number of crawled websites is printed to the console.
5. The duplicated URLs are printed to the console.

## Example

Crawl up to 50 websites starting from `https://myxalandri.gr`:

```
python script-web-crawler.py --max-websites 50
```


## Note

Please ensure that you have the necessary permissions to write files in the directory where the script is executed. The script will create or overwrite `crawled_urls.txt` in the same directory.

