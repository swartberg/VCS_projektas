from bs4 import BeautifulSoup
import requests
import pandas as pd
from IPython.display import display

def scrape_website(url):
    html = requests.get(url)
    if html.status_code == 200:
        bs_html = BeautifulSoup(html.content, 'html.parser')

        all_products = bs_html.find("div", class_="catalog-taxons-products-container")
        product_name_all = all_products.find_all("a", class_="catalog-taxons-product__name")
        product_price_all = all_products.find_all("span", class_="catalog-taxons-product-price__item-price")

        list_product_name = []
        list_product_price = []

        for product_name in product_name_all:
            product_name_ok = product_name.text.strip()
            list_product_name.append(product_name_ok)

        for product_price in product_price_all:
            product_price_ok = product_price.text.strip().replace("\n", "").replace("/ vnt.", "").replace("€", " €")
            list_product_price.append(product_price_ok)

        df = pd.DataFrame()
        df["Name"] = list_product_name
        df["Price"] = list_product_price

        display(df)

base_url = "https://www.senukai.lt/c/tv-audio-video-zaidimu-kompiuteriai/televizoriai-ir-priedai/televizoriai/9h1"
url_pages = 5

for page_number in range(1, url_pages + 1):
    url = f"{base_url}?page={page_number}"
    scrape_website(url)


