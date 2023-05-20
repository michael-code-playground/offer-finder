import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import time
import csv
url = "https://www.ceneo.pl/Telefony_komorkowe/Pamiec_wewnetrzna:128_GB,256_GB;szukaj-oneplus.htm"
time.sleep(1)

end = False
while True:
    
    if end == True:
        break
    else:
        r = requests.get(url)
        doc = BeautifulSoup(r.text, "html.parser")

    #search through products
    for product in doc.select(".cat-prod-row"):
        price = product.select_one(".value").text
        link = product.select_one(".go-to-product").attrs["href"]
        memory = product.select(".cat-prod-row__params strong")[3].text
        
        #remove unwanted characters
        if " " in price:
            temp_price = price.split(" ")
        final_price = "".join(temp_price)
        
        offer = urljoin(url, link)
        
        #extract price, link to the offer, memory
        if int(final_price) <= 1500:
            print(f"{final_price} PLN")
            print(offer)
            print(memory)
            #put data in the csv file
            with open("phones.csv", 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';',quotechar='"')
                writer.writerow([final_price, offer, memory])
    
    #if there's the next page, go there
    try:
        next_page = doc.select_one(".pagination__next").attrs["href"]
    except AttributeError:
        print("You've reached the end of the scope of your search")
        end = True
    else:
        url = "https://www.ceneo.pl/"
        url = urljoin(url, next_page)
        time.sleep(1)
        
