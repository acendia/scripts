from bs4 import BeautifulSoup
import requests
import os 

class SchoolBookScraper:
    def __init__(self, url_file):
        self.urls = self.get_urls_from_file(url_file)

    @staticmethod
    def get_urls_from_file(file_name):
        with open(file_name, "r") as f:
            urls = f.readlines()
            urls = [x.strip() for x in urls]
        return urls

    def create_book_directory(self, book_name):
        """
        Inside a Directory called books create a directory for each book
        """
        # create a directory called "Books" if it doesn't exist already:
        if not os.path.exists('books'):
            os.makedirs('books')
        
        # inside the direcotry called "books" create a directory for each book (book_name)
        if not os.path.exists(f'books/{book_name}'):
            os.makedirs(f'books/{book_name}')
        
        # return the directory path of the book (book_name)
        return f'books/{book_name}'



    def scrape_urls(self, book_dir):
        for idx, url_page in enumerate(self.urls):
            book_section = url_page.split('/')[-1].split('.')[0]
            if book_section == '':
                book_section = '0'
            print('--------->', book_section)
            

            response = requests.get(url_page)            
            html_content = response.content

            soup = BeautifulSoup(html_content, 'html.parser')
            tags = soup.find_all('div', id='eclass_ebook_body')

            with open(f'{book_dir}/{book_section}.txt', "w") as myfile:
                for tag in tags:
                    for br in tag.find_all("br"):
                        if br.find_previous_sibling('br') is None and br.find_next_sibling('br') is None:
                            br.replace_with('\n')

                    for p in tag.find_all("p"):
                        p.insert(0, "\n")
                        p.append("\n")

                    for t in tag:
                        text = t.get_text().strip()
                        print(text + "\n")
                        myfile.write(text)
                        continue

if __name__ == "__main__":
    book_name = "economics_g"
    scraper = SchoolBookScraper("urls_"+book_name+".txt")
    book_dir = scraper.create_book_directory(book_name)
    scraper.scrape_urls(book_dir)
