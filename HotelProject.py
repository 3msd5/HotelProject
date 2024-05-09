import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar  # Tarih seçimi için
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
from datetime import datetime

# Ana uygulama penceresini oluştur
root = tk.Tk()
root.title("Otel Bulma")

# Pencere boyutunu ayarla
root.geometry("800x900")


# Gerekli değişkenleri tanımla
secilen_sehir = ""  # Seçilen şehri global olarak tanımlayın
giris_tarihi = ""
cikis_tarihi = ""

# Karanlık modu yönetmek için sınıf
class KaranlikMod:
    def __init__(self, root):
        self.root = root
        self.karanlik_modu = False

        # Karanlık modu açma / kapama düğmesi
        self.karanlik_modu_dugme = ttk.Button(root, text="Karanlık Modu", command=self.karanlik_modunu_degistir)
        self.karanlik_modu_dugme.pack(side="bottom", pady=10)

    def karanlik_modunu_degistir(self):
        if not self.karanlik_modu:
            self.karanlik_modu = True
            self.root.tk_setPalette(background='gray20', foreground='white')
            self.karanlik_modu_dugme.state(['pressed'])
            self.karanlik_modunu_uygula(self.root)
        else:
            self.karanlik_modu = False
            self.root.tk_setPalette(background='SystemButtonFace', foreground='black')
            self.karanlik_modu_dugme.state(['!pressed'])
            self.normal_modu_uygula(self.root)

    def karanlik_modunu_uygula(self, widget):
        if isinstance(widget, tk.Widget):
            widget.tk_setPalette(background='gray20', foreground='white')
        for child in widget.winfo_children():
            self.karanlik_modunu_uygula(child)

    def normal_modu_uygula(self, widget):
        if isinstance(widget, tk.Widget):
            widget.tk_setPalette(background='SystemButtonFace', foreground='black')
        for child in widget.winfo_children():
            self.normal_modu_uygula(child)

def giris_tiklandi():
    root.withdraw()  # Mevcut pencereyi gizle
    rezervasyon_ekrani()

def cikis_yap():
    root.destroy()

def rezervasyon_ekrani():
    # Rezervasyon ekranını oluştur
    global secilen_sehir, giris_tarihi, cikis_tarihi

    rezervasyon_pencere = tk.Toplevel()
    rezervasyon_pencere.title("Rezervasyon Ekranı")
    rezervasyon_pencere.geometry("800x900")  # Pencere boyutunu ayarla

    # Karanlık modu özelliğini ekleyin
    karanlik_mod = KaranlikMod(rezervasyon_pencere)

    # Tarih ve saat gösterimi
    def update_clock():
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d/%m/%Y")
        clock_label.config(text=f"Tarih: {current_date}     Saat: {current_time}")
        rezervasyon_pencere.after(1000, update_clock)

    clock_label = tk.Label(rezervasyon_pencere, font=("Helvetica", 12))
    clock_label.pack()
    update_clock()

    # Şehir Seçimi
    tk.Label(rezervasyon_pencere, text="Şehir Seçiniz:", font=("Helvetica", 14, "bold")).pack()
    sehirler = ["Amsterdam", "Barselona", "Berlin", "Braga", "Lizbon", "Madrid", "Manchester", "Milano", "Paris",
                "Prag", "Roma", "Venedik", "Viyana", "Zürih"]
    secilen_sehir = sehirler[0]  # Başlangıçta ilk şehir seçili olacak
    sehirler_dropdown = ttk.Combobox(rezervasyon_pencere, values=sehirler, font=("Helvetica", 14))
    sehirler_dropdown.set(secilen_sehir)  # Başlangıçta seçilen şehri belirtin
    sehirler_dropdown.pack(pady=10)

    # Giriş Tarihi Seçimi
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

    # Çıkış Tarihi Seçimi
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
                if cikis_tarihi <= giris_tarihi:  # Çıkış tarihi giriş tarihinden önce olmamalı
                    messagebox.showerror("Hata", "Çıkış tarihi giriş tarihinden önce veya aynı olamaz!")
                    return
            c_tarih_win.destroy()

        c_tarih_onay_button = tk.Button(c_tarih_win, text="Onayla", command=c_tarih_onay, font=("Helvetica", 12))
        c_tarih_onay_button.pack(pady=10)

    c_tarih_sec_button = ttk.Button(rezervasyon_pencere, text='Çıkış Tarihi Seç', command=c_tarih_sec, style='TButton')
    c_tarih_sec_button.pack(pady=10)

    # Ödeme Şekli Seçimi
    tk.Label(rezervasyon_pencere, text="Ödeme Şekli Seçiniz*:", font=("Helvetica", 14, "bold")).pack()
    odeme_sekli = tk.StringVar()
    odeme_sekli.set("Euro")
    odeme_sekli_radio1 = ttk.Radiobutton(rezervasyon_pencere, text="€ - EURO", variable=odeme_sekli, value="Euro", style='TButton')
    odeme_sekli_radio1.pack()
    odeme_sekli_radio2 = ttk.Radiobutton(rezervasyon_pencere, text="₺ - TL", variable=odeme_sekli, value="TL", style='TButton')
    odeme_sekli_radio2.pack()

    # 1 Euro = 30 TL bilgisini ekleyelim
    tl_bilgisi_label = tk.Label(rezervasyon_pencere, text="*1 Euro = 30 TL", font=("Helvetica", 10))
    tl_bilgisi_label.pack()

    def check_inputs():
        if not giris_tarihi or not cikis_tarihi:
            messagebox.showerror("Hata", "Lütfen giriş ve çıkış tarihlerini seçin!")
            return False
        elif not odeme_sekli.get():
            messagebox.showerror("Hata", "Lütfen ödeme şeklini seçin!")
            return False
        else:
            return True

    def onayla():
        if not check_inputs():
            return
        global giris_tarihi, cikis_tarihi
        giris_tarihi_str = giris_tarihi
        cikis_tarihi_str = cikis_tarihi
        secilen_odeme_sekli = odeme_sekli.get()
        fiyat_mesaji = f"Fiyatlar: {'Euro' if secilen_odeme_sekli == 'Euro' else 'TL'}"  # Ödeme şekline göre fiyat mesajını belirle
        messagebox.showinfo("Rezervasyon Bilgileri",
                            f"Seçilen Şehir: {secilen_sehir}\n"
                            f"Giriş Tarihi: {giris_tarihi_str}\n"
                            f"Çıkış Tarihi: {cikis_tarihi_str}\n"
                            f"Ödeme Şekli: {secilen_odeme_sekli}\n\n"
                            f"{fiyat_mesaji}")
        # Otel verilerini göster
        show_hotels()

    onay_butonu = ttk.Button(rezervasyon_pencere, text="Onayla", command=onayla)
    onay_butonu.pack(pady=10)

    def scrape_hotels(city, checkin, checkout):
        url = f'https://www.booking.com/searchresults.html?ss={city}&checkin={checkin}&checkout={checkout}&group_adults=2&no_rooms=1&group_children=0'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # HTTP hata durumlarını kontrol et
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
        except requests.exceptions.RequestException as e:
            print(f"İstek hatası: {e}")
            return []

    def show_hotels():
        city = secilen_sehir
        checkin = giris_tarihi
        checkout = cikis_tarihi
        hotels_data = scrape_hotels(city, checkin, checkout)
        if not hotels_data:
            messagebox.showerror("Hata", "Veri bulunamadı. Lütfen farklı bir tarih veya şehir seçin.")
            return

        # Otelleri TXT dosyasına kaydet
        with open('myhotels.txt', 'w', encoding='utf-8') as txtfile:
            for hotel in hotels_data:
                txtfile.write(f"Otel Adı: {hotel['name']}\n")
                txtfile.write(f"Adres: {hotel['address']}\n")
                txtfile.write(f"Mesafe: {hotel['distance']}\n")
                txtfile.write(f"Puan: {hotel['rating']}\n")
                txtfile.write(f"Fiyat: {hotel['price']}\n\n")

        # Top 5 otelleri GUI'de göster
        display_top_hotels(hotels_data)

    def display_top_hotels(top_hotels):
        top_hotels_text.delete('1.0', tk.END)  # Önceki içeriği temizle
        for hotel in top_hotels:
            top_hotels_text.insert(tk.END, f"Otel Adı: {hotel['name']}\n")
            top_hotels_text.insert(tk.END, f"Adres: {hotel['address']}\n")
            top_hotels_text.insert(tk.END, f"Mesafe: {hotel['distance']}\n")
            top_hotels_text.insert(tk.END, f"Puan: {hotel['rating']}\n")
            top_hotels_text.insert(tk.END, f"Fiyat: {hotel['price']}\n\n")


    # Top 5 Otelleri Gösterme Alanı
    top_hotels_frame = tk.Frame(rezervasyon_pencere)
    top_hotels_frame.pack(pady=20)

    top_hotels_label = tk.Label(top_hotels_frame, text="En İyi 5 Otel:", font=("Helvetica", 16, "bold"))
    top_hotels_label.pack()

    top_hotels_text = tk.Text(top_hotels_frame, height=12, width=70)
    top_hotels_text.pack()



    cikis_butonu = ttk.Button(rezervasyon_pencere, text="Çıkış", command=rezervasyon_pencere.destroy)
    cikis_butonu.pack(side="bottom", pady=10)

    geri_butonu = ttk.Button(rezervasyon_pencere, text="Geri", command=root.deiconify)
    geri_butonu.pack(side="bottom", pady=10)

# Hoşgeldiniz metnini oluştur
hosgeldiniz_metni = tk.Label(root, text="Otel Bulma Programına Hoşgeldiniz", font=("Helvetica", 20, "bold"), pady=20)
hosgeldiniz_metni.pack()

# Karanlık modu özelliğini ekleyin
karanlik_mod = KaranlikMod(root)

# Giriş Butonu
giris_butonu = ttk.Button(root, text="Rezervasyon Yapmak için Tıklayınız", command=giris_tiklandi)
giris_butonu.pack(pady=20)

# Çıkış Butonu
cikis_butonu = ttk.Button(root, text="Çıkış", command=cikis_yap)
cikis_butonu.pack(side="bottom",pady=20)

root.mainloop()