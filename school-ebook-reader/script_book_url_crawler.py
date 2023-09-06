import requests
from bs4 import BeautifulSoup

# Not needed anymore. Only used to collect all the urls from each book.

def main():
    base_url = 'http://ebooks.edu.gr/ebooks/v/html/8547/2007/Meleti-Perivallontos_A-Dimotikou_html-apli/index.html'
    file_name = 'book_urls/'+'urls_meleti_perivallontos_a_dimotikou.txt'
    
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    option_tags = soup.find_all('option')

    url_list = []
    # extract urls from option tags
    for option_tag in option_tags:
        url_list.append('http://ebooks.edu.gr/ebooks/v/html/8547/2007/Meleti-Perivallontos_A-Dimotikou_html-apli/'+option_tag['value'])
        
    # write url content to the file
    open(file_name, 'w').close()

    for url in url_list:
        with open(file_name, "a") as f:
            if url == url_list[-1]:
                f.write(url)    
            else:
                f.write(url + '\n')
        

    # remove duplicates from the file
    with open(file_name, 'r') as file:
            lines = file.readlines()

    unique_lines = list(dict.fromkeys(lines))

    with open(file_name, 'w') as file:
        file.writelines(unique_lines)


if __name__ == "__main__":
    ### !!!!!!!! This script is not needed anymore. Only used to collect all the urls from each book !!!!!!!!!!!
    # main()
    pass