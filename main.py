from bs4 import BeautifulSoup
import requests
import pandas as pd
from IPython.display import display

combined_df = pd.DataFrame()

def brand_selector():
    selected_brand = input("Select brand: ")
    brand_url = ""
    
    if selected_brand.isalpha() == False:
        print("Please enter a valid brand name")
        return None
    elif selected_brand.lower() == "apple":
        brand_url = f"{base_url}?f=k99p"
    elif selected_brand.lower() == "samsung":
        brand_url = f"{base_url}?f=k1xe"
    else:
        print("Brand not recognized")
        return None
    
    return brand_url  

def scrape_website(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    html = requests.get(url=url, headers=headers)
    bs_html = BeautifulSoup(html.content, "html.parser")

    all_products = bs_html.find("div", attrs={"class":"catalog-taxons-products-container__grid-row"})
    products_info = all_products.findAll("div", attrs={"class":"catalog-taxons-product__hover"})

    list_product_name = []
    list_product_price = []
    
    for idx in range(0, len(products_info)):
        product_name = products_info[idx].img["alt"].replace("Mobilusis telefonas ", "")
        product_price = products_info[idx].span.text.strip().replace("\n", "").replace("/ vnt.", "").replace("€", "").replace(",", ".").replace(" ", "")
        list_product_name.append(product_name)
        list_product_price.append(float(product_price))
    
    df["Name"] = list_product_name
    df["Price"] = list_product_price

base_url = "https://www.senukai.lt/c/telefonai-plansetiniai-kompiuteriai/mobilieji-telefonai/5nt"
url_pages = 1

brand_url = None

while brand_url is None:
    brand_url = brand_selector()

for page_number in range(1, url_pages + 1):
    url = f"{brand_url}&page={page_number}"
    df = pd.DataFrame()
    scrape_website(url)
    combined_df = pd.concat([combined_df, df], ignore_index=True)

avg_price = combined_df['Price'].mean()
avg_result = f"The average price is {round(avg_price, 2)} €"

min_price = combined_df["Price"].min()
min_index = combined_df['Price'].idxmin()
min_row = combined_df.loc[min_index, "Name"]
min_result = f"The lowest price is {min_price} €:\n {min_row}\n"

max_price = combined_df["Price"].max()
max_index = combined_df['Price'].idxmax()
max_row = combined_df.loc[max_index, "Name"]
max_result = f"The highest price is {max_price} €:\n {max_row}\n"

print(min_result, '\n', max_result, '\n', avg_result)
display(combined_df)

html_file = "results.html"
combined_df.to_html(html_file, index=True)