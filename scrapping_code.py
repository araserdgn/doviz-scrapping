import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

def prices_pull():

    url ='https://bigpara.hurriyet.com.tr/doviz/'
    response = requests.get(url)

    if response.status_code == 200: #200 dönerse veri çekebilirsin demek
        soup = BeautifulSoup(response.content , 'html.parser') # Siteyi düzenle ve içerikleri html parçalarına böl
        ul_list =soup.findall('ul',style=True) # gelen html'lerden bütün ul olup içi dolu olanları topla
        prices=[]

        for ul in ul_list:
            currency_element = ul.find('li',class_='cell010 tal') #parçalanmış html'de ul listelerinin içinde li etiketi olan sınıf adı cell010 tal olan li'leri al

            if currency_element: #eğer li etiketi varsa
                currency_type = currency_element.text.strip() #text'ini al strip ile sağdan soldan boşlukları kaldır
                sell_price_element = ul.find_all('li', class_="cell015")

                if sell_price_element and len(sell_price_element) > 1 : #elementin içinde veri varsa demek
                    sell_price = float(sell_price_element[1].text.strip().replace(',','.')) #para birimindeki , yerine . seçiyoruz
                    prices.append((currency_type,sell_price))
        return prices