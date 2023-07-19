# Web Scraping and Data Extraction

This Python script performs web scraping and data extraction from a list of URLs provided in a `sitemaps.txt` file. The script utilizes the BeautifulSoup library to parse the HTML content of each URL, extract relevant information, and organize the data into directories for further analysis.

## Prerequisites

Make sure you have the following installed:

- Python (3.x)
- BeautifulSoup library
- Requests library

You can install the dependencies using pip:

```bash
pip install -r requirements.txt
```


## Installation

You can install the required libraries using pip:

```bash
pip install beautifulsoup4 requests
```

## Usage

1. Place the URLs you want to scrape in a file named `sitemaps.txt`. Each URL should be on a separate line.
2. Run the script using the following command:

```bash
python script_data_scraping.py
```

## Functionality

The script consists of the following main functions:

### 1. `create_directories(site_maps_file, delete_existing_directories=False)`

This function reads the URLs from the `site_maps_file` and creates directories to store the HTML, TXT, and metadata files for each domain in the URLs.

- `site_maps_file`: The path to the `sitemaps.txt` file containing the URLs.
- `delete_existing_directories`: Set to `True` if you want to delete existing directories and create new ones.

### 2. `is_index_page(soup, tag)`

This function checks if the given URL's HTML content represents an index page by searching for a specific meta tag named "author."

### 3. `extract_html(html_document, domain_dot_tld, idx_file)`

This function extracts the HTML content from the given URL and saves it to a file.

### 4. `extract_headline_and_description(soup, domain_dot_tld, idx_file)`

This function extracts the headline and description from the JSON data in the HTML content and saves them to a `.txt` file.

### 5. `extract_metadata(soup, domain_dot_tld, idx_file)`

This function extracts metadata from the HTML content and saves it to a `.meta` file in JSON format.

### 6. `create_zip_file(directory_list, zip_file_name="mydirectories.zip")`

This function compresses the created directories into a zip file.

## Note

- The script limits the number of pages processed to 50 (can be changed as needed).
- It skips front pages and index pages during extraction.

## Additional Information

- The script will display information about the extracted files, including the number of article pages, index pages, and their percentage.
- The resulting directories and files will be stored in the appropriate domain folders (e.g., `example.com/html_files`, `example.com/txt_files`, `example.com/metadata_files`).

Please ensure that you have the necessary permissions to access the URLs provided in the `sitemaps.txt` file, and use this script responsibly and in accordance with the website's terms of service. Happy data extraction!

