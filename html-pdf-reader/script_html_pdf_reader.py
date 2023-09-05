from bs4 import BeautifulSoup
import requests
import os 

class SchoolBookScraper:
    def __init__(self, url_file):
        self.urls = self.get_urls_from_file(url_file)

    @staticmethod
    def get_urls_from_file(file_name):
        with open('book_urls/'+file_name, "r") as f:
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
                book_section = 'index0'
            print('--------->', book_section)
            
            print('--->', url_page)
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
    # read all the books from the all_books.txt file and create a list of books (no function)
    list_of_books = []
    with open("all_books.txt", "r") as f:
        books = f.readlines()
        books = [x.strip() for x in books]
        for book in books:
            list_of_books.append(book)

    print(list_of_books)
    
    for book_name in list_of_books:
        scraper = SchoolBookScraper("urls_"+book_name+".txt")
        book_dir = scraper.create_book_directory(book_name)
        print(book_name)
        scraper.scrape_urls(book_dir)

