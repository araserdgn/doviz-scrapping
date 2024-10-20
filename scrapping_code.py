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
                instant_label = tk.Label(result_canvas_frame, text="Anlık Fiyat", font=("Arial",12),bg="#bd8633",fg="white", anchor="w")
                instant_label.grid(row=0 , column=1, padx=10 , pady=5, sticky="w") # Anlık label yazısı
                pay_can_label = tk.Label(result_canvas_frame, text="Alınabilecek Miktar", font=("Arial",12),bg="#d73343",fg="white", anchor="w")
                pay_can_label.grid(row=0 , column=2, padx=10 , pady=5, sticky="w") # alınacak miktar yazısı
                currency_label = tk.Label(result_canvas_frame, text=currency_type, font=("Arial",12), anchor="w")
                currency_label.grid(row=i+1 , column=0, padx=10 , pady=5, sticky="w") # Label'ı yani para biriminin ismini canvas'da yerleştirdik
                instant_price = tk.Label(result_canvas_frame, text=sell_price, font=("Arial", 12), anchor="w") #anlık olarak para birimi fiyatını yerlestrdk
                instant_price.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
                amount_label = tk.Label(result_canvas_frame, text=f'{pay_amount:.2f}', font=("Arial",12, "bold"), anchor="center")
                amount_label.grid(row=i+1 , column=2, padx=10 , pady=5, sticky="nsew") # satın alınacak miktarı yerleştirdk
            # scrooll ayarlar
            result_canvas.update_idletasks()
            result_canvas.config(scrollregion=result_canvas.bbox("all"))
    except ValueError:
        messagebox.showerror("Hata", "Litfen geçerli TL miktarı giriniz.")

# Tkinder arayüz
root = tk.Tk()
root.title('Currency Calculator')
root.geometry('500x500')
root.config(bg="#e6e6fa")

# baslık
title_label = tk.Label(root, text="Currency Calculator", font=("Arial", 24, "bold"), bg="#e6e6fa")
title_label.pack(pady=20)

# yatırım miktar girişi
entry_frame = tk.Frame(root, bg="#e6e6fa")
entry_frame.pack(pady=10)
entry_label = tk.Label(entry_frame, text="Yatırılacak (TL) Miktarı :", font=("Arial",14) ,bg="#e6e6fa")
entry_label.grid(row=0, column=0, padx=5)
entry_investmen = tk.Entry(entry_frame, font=("Arial",14), width=10)
entry_investmen.grid(row=0,column=1, padx=5)

# Hesaplama butonu
calculate_button = tk.Button(root, text="Hesapla", font=("Arial",14), command=calculator, bg="#4CAF50", fg="white")
calculate_button.pack(pady=20)

# Sonuçlar için bir frame kısmı tasarımı
result_frame = tk.Frame(root, bg="#f0f0f0", bd=2, relief="solid")
result_frame.pack(pady=10, fill="both")

# canvas ekleme kısmı
result_canvas = tk.Canvas(result_frame, bg="#f0f0f0")
result_canvas.pack(side="left", fill="both", expand=True) # expand ile veri var ise frame içini doldurması komutunu ekledk

# Scroll bar ekliyoruz
scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=result_canvas.yview)
scrollbar.pack(side="right", fill="y")

# sccrol'u canvas'a ekliyoruz
result_canvas.configure(yscrollcommand=scrollbar.set)

result_canvas_frame = tk.Frame(result_canvas, bg="#f0f0f0")
result_canvas.create_window((0,0), window=result_canvas_frame, anchor="nw")

root.mainloop()