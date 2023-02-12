import csv
import requests
from bs4 import BeautifulSoup


def benchmark(func):
    def wrapper():
        import time
        start = time.time()
        func()
        finish = time.time()
        print(f'Время выполнения функции {func.__name__}, заняло: {finish - start}')
    return wrapper


def get_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url, headers=headers)
    return response.text


def write_to_csv(data):
    with open('items.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['title'], data['price'], data['photo']))


def prepare_csv():
    with open('items.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(('Название', 'Цена', 'Фото'))


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages_ul = soup.find('nav', class_='woocommerce-pagination').find('ul', class_='page-numbers')
    last_page = pages_ul.find_all('li')[-2]
    total_pages = last_page.find('a').get('href').split('page/')[-1]
    tot = total_pages.split('/')[0]
    return int(tot)


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('ul', class_='products columns-4')
    products = product_list.find_all('li')
    # photo, title, price
    for product in products:
        try:
            photo = product.find('img', class_='attachment-woocommerce_thumbnail size-woocommerce_thumbnail').get('src')
        except:
            photo = ''

        try:
            title = product.find('h2', class_='woocommerce-loop-product__title').text
        except:
            title = ''

        try:
            import re
            price = product.find('bdi').text
            price = re.sub(r'[^\d,.]', '', price).split('.')[0] + ' сом'
        except:
            price = ''
    #
        data = {'title': title, 'price': price, 'photo': photo}
        write_to_csv(data)


@benchmark
def main():
    goods_url = 'https://alex.kg/product-category/turisticheskoe-snaryazhenie/'
    pages = '?pages='
    total_pages = get_total_pages(get_html(goods_url))
    prepare_csv()
    for page in range(1, total_pages+1):
        url_with_page = goods_url + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)


if __name__ == '__main__':
    main()
