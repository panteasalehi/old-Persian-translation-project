import os

import requests
from bs4 import BeautifulSoup


def findimage(url):
    url2 = "https://www.livius.org/articles/person/ariaramnes/"
    url = url.strip()
    base_directory = 'data'
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    folder_name = url.split("/")[-2]
    full_path = os.path.join(base_directory, folder_name)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')

    text = soup.find_all('ol')
    result_Txt = url + str(text).replace("<li><font face=\"Arial,Helvetica\"><font size=\"-1\">", "").replace(
        "</font></font></li>", "").replace("[<ol>", "").replace("</ol>]", "")

    file_path = os.path.join(full_path, base_directory.replace(' ', '-').replace('/', '') + '.txt')  
    with open(file_path, 'w', encoding='utf-8') as f: 
        f.write(result_Txt)

    for image in images:
        name = image['src'].split('/')[-1]  
        link = "https://www.livius.org" + image['src']  
        file_path = os.path.join(full_path, name.replace(' ', '-').replace('/', '') + '.jpg')

        with open(file_path, 'wb') as f:
            im = requests.get(link)
            f.write(im.content)

    print(f"Images saved to folder: {full_path}")


def main():
    url = 'https://www.livius.org/sources/content/achaemenid-royal-inscriptions/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    second_table = tables[1] 

    for url_data in second_table.find_all('a'):
        if url_data.has_attr('href'):
            if not url_data['href'].startswith("https"):
                url_data['href'] = "https://www.livius.org"+url_data['href']
            findimage(url_data['href'])


if __name__ == "__main__":
    main()
