import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

def prices_pull():

    url ='https://bigpara.hurriyet.com.tr/doviz/'
    response = requests.get(url)

    if response.status_code == 200: #200 dönerse veri çekebilirsin demek
        soup = BeautifulSoup(response.content , 'html.parser') # Siteyi düzenle ve içerikleri html parçalarına böl
        ul_list =soup.find_all('ul',style=True) # gelen html'lerden bütün ul olup içi dolu olanları topla
        prices=[]

        for ul in ul_list:
            currency_element = ul.find('li',class_='cell010 tal') #parçalanmış html'de ul listelerinin içinde li etiketi olan sınıf adı cell010 tal olan li'leri al

            if currency_element: #eğer li etiketi varsa
                currency_type = currency_element.text.strip() #text'ini al strip ile sağdan soldan boşlukları kaldır
                sell_price_element = ul.find_all('li', class_="cell015")

                if sell_price_element and len(sell_price_element) > 1 : #elementin içinde veri varsa demek
                    sell_price = float(sell_price_element[1].text.strip().replace(',','.')) #para birimindeki , yerine . seçiyoruz
                    prices.append((currency_type,sell_price)) #prices array içine para birim adı ve tutarını
        return prices
    else:
        messagebox.showerror("Hata , dövizler çekilemedi.")

def calculator():
    try:
        tl_amount = float(entry_investmen.get())
        prices = prices_pull()

        if prices:
            for widget in result_canvas_frame.winfo_children():
                widget.destroy()
            for i ,(currency_type, sell_price) in enumerate(prices): #enumarate sıralı olarak gelemsini sağlar
                pay_amount = tl_amount/sell_price
                currency_label = tk.Label(result_canvas_frame, text=currency_type, font=("Arial",12), anchor="w")
                currency_label.grid(row=i , column=0, padx=10 , pady=5, sticky="w") # Label'ı yani para birimini canvas'da yerleştirdik
                amount_label = tk.Label(result_canvas_frame, text=f'{pay_amount:.2f}', font=("Arial",12), anchor="e")
                amount_label.grid(row=i , column=1, padx=10 , pady=5, sticky="e")
            # scrooll ayarlar
            result_canvas.update_idletasks()
            result_canvas.config(scrollregion=result_canvas.bbox("all"))
    except ValueError:
        messagebox.showerror("Hata", "Litfen geçerli TL miktarı giriniz.")