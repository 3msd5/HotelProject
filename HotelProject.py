import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

class KaranlikMod:
    def __init__(self, root):
        self.root = root
        self.karanlik_mod = False

        self.karanlik_mod_dugme = ttk.Button(root, text="Karanlık Mod", command=self.toggle_karanlik_mod)
        self.karanlik_mod_dugme.pack(side="bottom", pady=10)

    def toggle_karanlik_mod(self):
        if not self.karanlik_mod:
            self.karanlik_mod = True
            self.root.tk_setPalette(background='gray20', foreground='white')
            self.karanlik_mod_dugme.state(['pressed'])
            self.apply_karanlik_mod(self.root)
        else:
            self.karanlik_mod = False
            self.root.tk_setPalette(background='SystemButtonFace', foreground='black')
            self.karanlik_mod_dugme.state(['!pressed'])
            self.apply_normal_mod(self.root)

    def apply_karanlik_mod(self, widget):
        if isinstance(widget, tk.Widget):
            widget.tk_setPalette(background='gray20', foreground='white')
        for child in widget.winfo_children():
            self.apply_karanlik_mod(child)

    def apply_normal_mod(self, widget):
        if isinstance(widget, tk.Widget):
            widget.tk_setPalette(background='SystemButtonFace', foreground='black')
        for child in widget.winfo_children():
            self.apply_normal_mod(child)

secilen_sehir = None  # StringVar olarak tanımlayalım
giris_tarihi = ""
cikis_tarihi = ""

def giris_tiklandi():
    global secilen_sehir
    secilen_sehir = tk.StringVar()  # StringVar'ı burada oluşturun
    root.withdraw()
    rezervasyon_ekrani()

def rezervasyon_ekrani():
    def geri_git():
        rezervasyon_pencere.destroy()
        root.deiconify()

    def cikis_yap():
        rezervasyon_pencere.destroy()
        root.destroy()

    global secilen_sehir, giris_tarihi, cikis_tarihi

    rezervasyon_pencere = tk.Toplevel()
    rezervasyon_pencere.title("Rezervasyon Ekranı")
    rezervasyon_pencere.geometry("800x900")

    karanlik_mod = KaranlikMod(rezervasyon_pencere)

    tk.Label(rezervasyon_pencere, text="Şehir Seçiniz:", font=("Helvetica", 14, "bold")).pack()
    sehirler = ["Amsterdam", "Barcelona", "Berlin","Braga","Lizbon","Madrid","Manchester","Milano","Paris", "Prag", "Roma", "Venedik", "Viyana", "Zürih"]
    secilen_sehir.set(sehirler[0])
    sehirler_dropdown = ttk.Combobox(rezervasyon_pencere, textvariable=secilen_sehir, values=sehirler, font=("Helvetica", 14))
    sehirler_dropdown.pack(pady=10)
    if karanlik_mod.karanlik_mod:
        sehirler_dropdown.config(foreground='grey')

    tk.Label(rezervasyon_pencere, text="Giriş Tarihi Seçiniz:", font=("Helvetica", 14, "bold")).pack()
    g_tarih = tk.StringVar()
    g_tarih_label = tk.Label(rezervasyon_pencere, textvariable=g_tarih, font=("Helvetica", 12))
    g_tarih_label.pack()
    def g_tarih_sec():
        g_tarih_win = tk.Toplevel()
        cal = Calendar(g_tarih_win, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(padx=20, pady=20)
        def g_tarih_onay():
            global giris_tarihi
            giris_tarihi = cal.get_date()
            g_tarih.set(giris_tarihi)
            g_tarih_win.destroy()
        g_tarih_onay_button = tk.Button(g_tarih_win, text="Onayla", command=g_tarih_onay, font=("Helvetica", 12))
        g_tarih_onay_button.pack(pady=10)
    g_tarih_sec_button = ttk.Button(rezervasyon_pencere, text='Giriş Tarihi Seç', command=g_tarih_sec, style='TButton')
    g_tarih_sec_button.pack(pady=10)

    tk.Label(rezervasyon_pencere, text="Çıkış Tarihi Seçiniz:", font=("Helvetica", 14, "bold")).pack()
    c_tarih = tk.StringVar()
    c_tarih_label = tk.Label(rezervasyon_pencere, textvariable=c_tarih, font=("Helvetica", 12))
    c_tarih_label.pack()
    def c_tarih_sec():
        c_tarih_win = tk.Toplevel()
        cal = Calendar(c_tarih_win, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(padx=20, pady=20)
        def c_tarih_onay():
            global cikis_tarihi
            cikis_tarihi = cal.get_date()
            c_tarih.set(cikis_tarihi)
            if giris_tarihi and cikis_tarihi:
                if cikis_tarihi <= giris_tarihi:
                    messagebox.showerror("Hata", "Çıkış tarihi giriş tarihinden önce olamaz!")
                    return
            c_tarih_win.destroy()
        c_tarih_onay_button = tk.Button(c_tarih_win, text="Onayla", command=c_tarih_onay, font=("Helvetica", 12))
        c_tarih_onay_button.pack(pady=10)
    c_tarih_sec_button = ttk.Button(rezervasyon_pencere, text='Çıkış Tarihi Seç', command=c_tarih_sec, style='TButton')
    c_tarih_sec_button.pack(pady=10)

    tk.Label(rezervasyon_pencere, text="Ödeme Şekli Seçiniz*:", font=("Helvetica", 14, "bold")).pack()
    odeme_sekli = tk.StringVar()
    odeme_sekli.set("Euro")
    odeme_sekli_radio1 = ttk.Radiobutton(rezervasyon_pencere, text="€ - EURO", variable=odeme_sekli, value="Euro", style='TButton')
    odeme_sekli_radio1.pack()
    odeme_sekli_radio2 = ttk.Radiobutton(rezervasyon_pencere, text="₺ - TL", variable=odeme_sekli, value="TL", style='TButton')
    odeme_sekli_radio2.pack()

    tl_bilgisi_label = tk.Label(rezervasyon_pencere, text="*1 Euro = 30 TL", font=("Helvetica", 10))
    tl_bilgisi_label.pack()

    def onayla():
        global secilen_sehir, giris_tarihi, cikis_tarihi
        secilen_sehir = secilen_sehir.get()  # Burada .get() kullanarak değeri alıyoruz
        giris_tarihi_str = giris_tarihi
        cikis_tarihi_str = cikis_tarihi
        secilen_odeme_sekli = odeme_sekli.get()
        fiyat_mesaji = f"Fiyatlar: {'Euro' if secilen_odeme_sekli == 'Euro' else 'TL'}"
        messagebox.showinfo("Rezervasyon Bilgileri",
                            f"Seçilen Şehir: {secilen_sehir}\n"
                            f"Giriş Tarihi: {giris_tarihi_str}\n"
                            f"Çıkış Tarihi: {cikis_tarihi_str}\n"
                            f"Ödeme Şekli: {secilen_odeme_sekli}\n\n"
                            f"{fiyat_mesaji}")
        show_hotels()

    onay_butonu = ttk.Button(rezervasyon_pencere, text="Onayla", command=onayla)
    onay_butonu.pack(pady=10)

    cikis_butonu = ttk.Button(rezervasyon_pencere, text="Çıkış", command=cikis_yap)
    cikis_butonu.pack(side="bottom", pady=10)

    geri_butonu = ttk.Button(rezervasyon_pencere, text="Geri", command=geri_git)
    geri_butonu.pack(side="bottom", pady=10)

def scrape_hotels(city, checkin, checkout):
    url = f'https://www.booking.com/searchresults.html?ss={city}&checkin={checkin}&checkout={checkout}&group_adults=2&no_rooms=1&group_children=0'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    hotels = soup.findAll('div', {'data-testid': 'property-card'})
    hotels_data = []
    for hotel in hotels:
        name_element = hotel.find('div', {'data-testid': 'title'})
        address_element = hotel.find('a', {'data-testid': 'address'})
        distance_element = hotel.find('span', {'data-testid': 'distance-time'})
        rating_element = hotel.find('span', {'data-testid': 'content-hotel-rating'})
        price_element = hotel.find('div', {'data-testid': 'price-excluding-x-price-strikeout'})
        name = name_element.text.strip() if name_element else "NOT GIVEN"
        address = address_element.text.strip() if address_element else "NOT GIVEN"
        distance = distance_element.text.strip() if distance_element else "NOT GIVEN"
        rating = rating_element.text.strip() if rating_element else "NOT GIVEN"
        price = price_element.text.strip() if price_element else "NOT GIVEN"
        hotels_data.append({
            'name': name,
            'address': address,
            'distance': distance,
            'rating': rating,
            'price': price
        })
    return hotels_data

def show_hotels():
    city = secilen_sehir
    checkin = giris_tarihi
    checkout = cikis_tarihi
    hotels_data = scrape_hotels(city, checkin, checkout)
    with open('myhotels.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'address', 'distance', 'rating', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for hotel in hotels_data:
            writer.writerow(hotel)

root = tk.Tk()
root.title("Otel Bulma")
root.geometry("800x900")

hosgeldiniz_metni = tk.Label(root, text="Otel Bulma Programına Hoşgeldiniz",
                             font=("Helvetica", 25, "bold"),
                             fg="Black",justify="center")
hosgeldiniz_metni.pack(pady=50)

giris_butonu = ttk.Button(root, text="Giriş", command=giris_tiklandi)
giris_butonu.pack(pady=75)

cikis_butonu = ttk.Button(root, text="Çıkış", command=root.destroy)
cikis_butonu.pack(side="bottom", pady=10)

karanlik_mod = KaranlikMod(root)

root.mainloop()
