import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages_div = soup.find('div', class_='pageToInsert')
    last_page = pages_div.find_all('a')[-2]
    total_pages = last_page.get('href').split('=')[-1]
    return int(total_pages)


def write_to_csv(data):
    with open('wildberies_notebooks.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow((data['title'],
                         data['price'],
                         data['characters']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div', class_='catalog_main_table j-products-container')
    products = product_list.find_all('div', class_='dtList i-dtList j-card-item')
    
    
    for product in products:
        try:
            title = product.find('div', class_='dtlist-inner-brand-name').find('strong', class_='brand-name c-text-sm').text
        except:
            title = ''

        try:
            price = product.find('span', class_='price').find('ins', class_='lower-price').text
        except: 
            price = ''   
        
        try:
            characters = product.find('span', class_='goods-name c-text-sm').text
        except:
            characters = ''

        data = {'title': title, 'price': price, 'characters': characters}
        write_to_csv(data)

def main():
    notebooks_url = "https://www.wildberries.kg/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki"
    pages = "?page="
    
    total_pages = get_total_pages(get_html(notebooks_url))
    # print(total_pages)
    for page in range(1, total_pages+1): 
        url_with_page = notebooks_url + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)

main()