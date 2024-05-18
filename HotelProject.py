import tkinter as tk # gui
from tkinter import ttk, messagebox #uyarı mesajları
from tkcalendar import Calendar  # Tarih seçimi için
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from PIL import Image, ImageTk  # resimler için
import io
import webbrowser # şehir bilgileri url si için

# Ana uygulama penceresini oluştur
root = tk.Tk()
root.title("Finding Cheapest Hotel")
root.geometry("800x900")
# Stil oluştur
style = ttk.Style()
#style.theme_use('clam')  # tkinter içindeki en modern tema


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
        self.karanlik_modu_dugme = ttk.Button(root, text="Dark Mode", command=self.karanlik_modunu_degistir)
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
            if isinstance(widget, ttk.Radiobutton):
                widget.tk_setPalette(background='gray20', foreground='white')
        for child in widget.winfo_children():
            self.karanlik_modunu_uygula(child)

    def normal_modu_uygula(self, widget):
        if isinstance(widget, tk.Widget):
            widget.tk_setPalette(background='SystemButtonFace', foreground='black')
            if isinstance(widget, ttk.Radiobutton):
                widget.tk_setPalette(background='SystemButtonFace', foreground='black')
        for child in widget.winfo_children():
            self.normal_modu_uygula(child)

    def open_instagram(self):
        webbrowser.open("https://www.instagram.com/3msd5")

def giris_tiklandi():
    root.withdraw()  # Mevcut pencereyi gizle
    rezervasyon_ekrani()

def cikis_yap():
    root.destroy()



def rezervasyon_ekrani():

    # Rezervasyon ekranını oluştur
    global secilen_sehir, giris_tarihi, cikis_tarihi

    rezervasyon_pencere = tk.Toplevel()
    rezervasyon_pencere.title("Reservation Screen")
    rezervasyon_pencere.geometry("800x900")  # Pencere boyutunu ayarla

    # Karanlık modu özelliğini ekleyin
    karanlik_mod = KaranlikMod(rezervasyon_pencere)

    # Tarih ve saat gösterimi
    def update_clock():
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%y-%m-%d")
        clock_label.config(text=f"Date: {current_date}     |     Time: {current_time}")
        rezervasyon_pencere.after(1000, update_clock)

    clock_label = tk.Label(rezervasyon_pencere, font=("Helvetica", 12))
    clock_label.pack()
    update_clock()

    secilen_sehir = None  # Başlangıçta hiçbir şehir seçili değil

    tk.Label(rezervasyon_pencere, text="Please Select City:", font=("Helvetica", 14, "bold")).pack()
    sehirler = ["Amsterdam", "Barcelona", "Berlin", "Braga", "Lisbon", "Madrid", "Manchester", "Milan", "Paris",
                "Prague", "Rome", "Venice", "Vienna", "Zurich"]
    sehirler_dropdown = ttk.Combobox(rezervasyon_pencere, values=sehirler, font=("Helvetica", 14))
    sehirler_dropdown.current(None)  # Başlangıçta seçili bir şehir yok
    sehirler_dropdown.pack(pady=10)

    def on_sehir_sec(*args):
        global secilen_sehir
        secilen_sehir = sehirler_dropdown.get()
        if secilen_sehir in sehir_bilgileri:
            bilgi_metni.config(text=sehir_bilgileri[secilen_sehir])
        else:
            bilgi_metni.config(text="No information about this city.")

    # Şehir bilgileri sözlüğü
    sehir_bilgileri = {
        "Amsterdam": "Founded in the 12th century as a fishing village on the banks of the river Amstel,\nAmsterdam is the largest city in the Netherlands in terms of population\nand the most important culturally and financially.",
        "Barcelona": "The second largest city in the North East of Spain. It is also the capital\nand largest city of the autonomous community of Catalonia. Barcelona, with its rich cultural\nheritage, is today an important cultural center and one of the most important tourist destinations.",
        "Berlin": "The capital and largest city of Germany, also a state.",
        "Braga": "It is the third largest city in Portugal and the largest city in the Minho Region.\nThe city is considered the religious center of the country.",
        "Lisbon": "Lisbon is the capital of Portugal. It is the largest city of this country in Europe.\nBuilt on the river formed by the Tejo River, Lisbon is located on the Atlantic Ocean coast.",
        "Madrid": "Spain's capital and most populous city. It is also the political,\neconomic and cultural center of the country.",
        "Manchester": "A city in the North-West region of England in the United Kingdom.\nIt is the sixth most populous city in the country.",
        "Milan": "The capital of the Lombardy region in northern Italy.\nMilan is the fashion and financial center of Italy.",
        "Paris": "The capital of France and the most populous city in the country.\nSince the 17th century, Paris has been one of Europe's most important\ncenters of finance, diplomacy, trade, fashion, gastronomy, science and art.",
        "Prague": "The capital and largest city of the Czech Republic, also\nknown as the ‘Golden City’, ‘Left Bank of the Nineties’, ‘Fairytale City’,\n‘Mother of Cities’ and ‘Heart of Europe’.",
        "Rome": "Rome is the capital and largest city of Italy.\nIt includes the Vatican City, the independent state where the Pope lives.",
        "Venice": "Venice is a famous city in northeastern Italy.\nIt is built on 118 islands separated by canals and connected by bridges.",
        "Vienna": "Vienna is the capital and most populous city of Austria.\nIt is the smallest in terms of area.",
        "Zurich": "Zurich is the largest city in Switzerland and an important cultural center.\nIt is the economic center of Switzerland and the cultural center of the\nGerman-speaking region. FIFA headquarters is located in Zurich."
    }

    # Şehir seçimi bileşenine işlevi bağlayın
    sehirler_dropdown.bind("<<ComboboxSelected>>", on_sehir_sec)

    # Şehir bilgisi metni
    bilgi_metni = tk.Label(rezervasyon_pencere, text="", font=("Helvetica", 12))
    bilgi_metni.pack(pady=10)

    def bilgi():
        if not secilen_sehir:
            messagebox.showinfo("Error", "Please select a city.")
            return
        bilgi_url = f"https://en.wikipedia.org/wiki/{secilen_sehir}"
        webbrowser.open(bilgi_url)

    bilgi_button = ttk.Button(rezervasyon_pencere, text="For more information about the city click here", command=bilgi)
    bilgi_button.pack(pady=10)

    # Giriş Tarihi Seçimi
    tk.Label(rezervasyon_pencere, text="Select Check-in Date:", font=("Helvetica", 14, "bold")).pack()
    g_tarih = tk.StringVar()
    g_tarih_label = tk.Label(rezervasyon_pencere, textvariable=g_tarih, font=("Helvetica", 12))
    g_tarih_label.pack()

    def g_tarih_sec():
        g_tarih_win = tk.Toplevel()
        cal = Calendar(g_tarih_win, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=20, pady=20)

        def g_tarih_onay():
            global giris_tarihi
            giris_tarihi = cal.get_date()
            g_tarih.set(giris_tarihi)
            g_tarih_win.destroy()

        g_tarih_onay_button = tk.Button(g_tarih_win, text="Confirm", command=g_tarih_onay, font=("Helvetica", 12))
        g_tarih_onay_button.pack(pady=10)

    g_tarih_sec_button = ttk.Button(rezervasyon_pencere, text='Select Check-in Date', command=g_tarih_sec, style='TButton')
    g_tarih_sec_button.pack(pady=10)

    # Çıkış Tarihi Seçimi
    tk.Label(rezervasyon_pencere, text="Select Check-out Date:", font=("Helvetica", 14, "bold")).pack()
    c_tarih = tk.StringVar()
    c_tarih_label = tk.Label(rezervasyon_pencere, textvariable=c_tarih, font=("Helvetica", 12))
    c_tarih_label.pack()

    def c_tarih_sec():
        c_tarih_win = tk.Toplevel()
        cal = Calendar(c_tarih_win, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=20, pady=20)

        def c_tarih_onay():
            global cikis_tarihi
            cikis_tarihi = cal.get_date()
            c_tarih.set(cikis_tarihi)
            if giris_tarihi and cikis_tarihi:
                if cikis_tarihi <= giris_tarihi:  # Çıkış tarihi giriş tarihinden önce olmamalı
                    messagebox.showerror("Error", "The release date cannot be before or the same as the entry date!")
                    return
            c_tarih_win.destroy()

        c_tarih_onay_button = tk.Button(c_tarih_win, text="Confirm", command=c_tarih_onay, font=("Helvetica", 12))
        c_tarih_onay_button.pack(pady=10)

    c_tarih_sec_button = ttk.Button(rezervasyon_pencere, text='Select Check-out Date', command=c_tarih_sec, style='TButton')
    c_tarih_sec_button.pack(pady=10)

    # Ödeme Şekli Seçimi
    tk.Label(rezervasyon_pencere, text="Choose Payment Method*:", font=("Helvetica", 14, "bold")).pack()
    odeme_sekli = tk.StringVar()

    odeme_sekli_radio1 = ttk.Radiobutton(rezervasyon_pencere, text="€ - EURO", variable=odeme_sekli, value="EUR", style='TRadiobutton')
    odeme_sekli_radio1.pack()
    odeme_sekli_radio2 = ttk.Radiobutton(rezervasyon_pencere, text="₺ - TL", variable=odeme_sekli, value="TRY", style='TRadiobutton')
    odeme_sekli_radio2.pack()

    # 1 Euro = 30 TL bilgisini ekleyelim
    tl_bilgisi_label = tk.Label(rezervasyon_pencere, text="*1 Euro = 30 TL", font=("Helvetica", 10))
    tl_bilgisi_label.pack()

    def check_inputs():
        global secilen_sehir, giris_tarihi, cikis_tarihi
        if not secilen_sehir:
            messagebox.showerror("Error", "Please select a city!")
            return False
        elif not giris_tarihi or not cikis_tarihi:
            messagebox.showerror("Error", "Please select the check-in and check-out dates!")
            return False
        elif not odeme_sekli.get():  # odeme_sekli'yi kontrol ederken get() fonksiyonunu kullanarak gerçek değeri alın
            messagebox.showerror("Error", "Please choose the payment method!")
            return False
        elif cikis_tarihi <= giris_tarihi:
            messagebox.showerror("Error", "The release date cannot be before or the same as the entry date!")
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
        fiyat_mesaji = f"Prices: {'Euro' if secilen_odeme_sekli == 'Euro' else 'TL'}"  # Ödeme şekline göre fiyat mesajını belirle
        messagebox.showinfo("Reservation Details",
                            f"Selected City: {secilen_sehir}\n"
                            f"Check-in Date: {giris_tarihi_str}\n"
                            f"Check-out Date: {cikis_tarihi_str}\n"
                            f"Payment Type: {secilen_odeme_sekli}\n\n"
                            )
        # Otel verilerini göster
        hotels_data = scrape_hotels(secilen_sehir, giris_tarihi_str, cikis_tarihi_str)


    onay_butonu = ttk.Button(rezervasyon_pencere, text="Confirm", command=onayla)
    onay_butonu.pack(pady=10)

    def get_label_for_city(city):
        url = f"https://www.booking.com/searchresults.en-gb.html?ss={city}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            label_element = soup.find('input', {'name': 'label'})
            if label_element:
                label_value = label_element['value']
                return label_value
            else:
                print(f"Label for {city} not found.")
        else:
            print(f"Request for {city} failed.")

    def scrape_hotels(selected_city, checkin, checkout):
        try:
            selected_label = get_label_for_city(selected_city)  # Seçilen şehir için label'ı al

            print("City: ", selected_city)  # secilen_sehir yerine selected_city kullanıldı
            print("Checkin:", checkin)
            print("Checkout:", checkout)
            print("Payment Type:", odeme_sekli.get())
            # Function to scrape hotel data from Booking.com

            base_url = "https://www.booking.com/searchresults.en-gb.html"
            selected_label = get_label_for_city(selected_city)  # Seçilen şehir için label'ı al

            query_params = {
                'label': selected_label,
                'sid': '75e30209011abe1aa1c492edf1647de4',
                'sb': '1',
                'sb_lp': '1',
                'src': 'index',
                'src_elem': 'sb',
                'error_url': 'https://www.booking.com/index.en-gb.html',
                'ss': selected_city,  # secilen_sehir yerine selected_city kullanıldı
                'checkin_monthday': checkin.split('-')[2],
                'checkin_month': checkin.split('-')[1],
                'checkin_year': checkin.split('-')[0],
                'checkout_monthday': checkout.split('-')[2],
                'checkout_month': checkout.split('-')[1],
                'checkout_year': checkout.split('-')[0],
                'group_adults': '2',
                'group_children': '0',
                'no_rooms': '1'
            }
            url2 = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in query_params.items()])}"

            # url = f"https://www.booking.com/searchresults.en-gb.html?ss={selected_city}&ssne={selected_city}&ssne_untouched={selected_city}&label={selected_label}&sid=75e30209011abe1aa1c492edf1647de4&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-1456928&dest_type=city&checkin={checkin}&checkout={checkout}&group_adults=2&no_rooms=1&group_children=0&selected_currency=EUR"
            url = (f"https://www.booking.com/searchresults.html"
                   f"?ss={selected_city}&checkin={checkin}&checkout={checkout}&group_adults=2&no_rooms=1&group_children=0&selected_currency=EUR")

            print("Check Url:",url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.9'
            }
            response = requests.get(url, headers=headers)

            response.raise_for_status()  # Raises an exception for 4XX or 5XX status codes
            soup = BeautifulSoup(response.text, 'html.parser')
            hotels_data = []

            count = 0  # İlk 10 otel için sayacı başlat

            for hotel in soup.findAll('div', {'data-testid': 'property-card'}):
                if count >= 10:  # Eğer ilk 10 otel alındıysa döngüyü sonlandır
                    break
                title_element = hotel.find('div', {'data-testid': 'title'})
                address_element = hotel.find('span', {'data-testid': 'address'})
                distance_element = hotel.find('span', {'data-testid': 'distance'})
                rating_element = hotel.find('div', {'data-testid': 'review-score'})
                price_element = hotel.find('span', {'class': 'f6431b446c fbfd7c1165 e84eb96b1f'})
                image_element = hotel.find('img', {'class': 'f9671d49b1'})  # Resim URL'lerini bul

                hotel_data = {
                    'Hotel Title': title_element.text.strip() if title_element else 'NOT GIVEN',
                    'Hotel Address': address_element.text.strip() if address_element else 'NOT GIVEN',
                    'Distance to City Center': distance_element.text.strip() if distance_element else 'NOT GIVEN',
                    'Hotel Rating': rating_element.text.strip() if rating_element else 'NOT GIVEN',
                    'Price': price_element.text.strip() if price_element else 'NOT GIVEN',
                    'Image URL': image_element['src'] if image_element else 'NOT GIVEN'
                }
                print(hotel_data)
                hotels_data.append(hotel_data)

                count += 1  # Sayacı artır

            # Para birimi seçimine göre fiyatları dönüştürme
            for hotel_data in hotels_data:
                if odeme_sekli.get() == "TRY" and '€' in hotel_data['Price']:
                    euro_price = float(hotel_data['Price'].replace('€', '').replace(',', '').strip())
                    tl_price = euro_price * 30  # 1 Euro = 30 TL dönüşümü
                    hotel_data['Price'] = f'{tl_price:.2f} TL'
                elif odeme_sekli.get() == "EUR" and '€' in hotel_data['Price']:
                    euro_price = float(hotel_data['Price'].replace('€', '').replace(',', '').strip())
                    hotel_data['Price'] = f'{euro_price:.2f} Euro'

            # Otel verilerini fiyatlarına göre sırala
            hotels_data.sort(key=lambda x: float(
                x['Price'].split()[0].replace('TL', '').replace('Euro', '').replace(',', '')) if 'TL' in x[
                'Price'] or 'Euro' in x['Price'] else float('inf'))

            # Otelleri TXT dosyasına kaydet
            with open('myhotels.txt', 'w', encoding='utf-8') as txtfile:
                for hotel in hotels_data:
                    txtfile.write(f"Hotel Name : {hotel['Hotel Title']}\n")
                    txtfile.write(f"Address    : {hotel['Hotel Address']}\n")
                    txtfile.write(f"Distance   : {hotel['Distance to City Center']}\n")
                    txtfile.write(f"Points     : {hotel['Hotel Rating']}\n")
                    txtfile.write(f"Price      : {hotel['Price']}\n\n")

                # En iyi 5 otelleri göstermek için yeni pencere oluştur
            display_top_hotels_window(hotels_data[:5])

            return hotels_data

        except requests.RequestException as e:
            messagebox.showerror("Error", f"There was a problem with internet connection: {str(e)}")
            return []





    def display_top_hotels_window(top_hotels):
        top_hotels_window = tk.Toplevel()
        top_hotels_window.title("Top 5 Cheapest Hotels")
        top_hotels_window.geometry("800x1050")

        top_hotels_frame = tk.Frame(top_hotels_window)
        top_hotels_frame.pack(pady=20)

        top_hotels_label = tk.Label(top_hotels_frame, text="Top 5 Cheapest Hotels:", font=("Helvetica", 16, "bold"))
        top_hotels_label.pack()

        # Resim alanı oluştur
        image_frame = tk.Frame(top_hotels_frame)
        image_frame.pack(side="left", fill="both", expand=True)
        # Metin alanı oluştur
        top_hotels_text = tk.Text(top_hotels_frame, height=30, width=60, font=("Helvetica", 12))
        top_hotels_text.pack(side="left", fill="both", expand=True)


        for hotel_index in range(5):  # Sadece ilk 5 oteli listele
            if hotel_index < len(top_hotels):
                hotel = top_hotels[hotel_index]

                top_hotels_text.insert(tk.END, f"\n\n************** {hotel_index + 1}. Otel **************\n"
                                               f"Hotel Name : {hotel['Hotel Title']}\n"
                                               f"Address    : {hotel['Hotel Address']}\n"
                                               f"Distance   : {hotel['Distance to City Center']}\n"
                                               f"Points     : {hotel['Hotel Rating']}\n"
                                               f"Price      : {hotel['Price']}\n\n")
                # Otel resimlerini yükle ve göster
                if hotel['Image URL']:
                    response = requests.get(hotel['Image URL'])
                    image_data = response.content
                    image = Image.open(io.BytesIO(image_data))
                    image = image.resize((141, 141),Image.Resampling.LANCZOS)  # ANTIALIAS yerine Image.Resampling.LANCZOS kullan
                    photo = ImageTk.PhotoImage(image)

                    image_label = tk.Label(image_frame, image=photo)
                    image_label.image = photo  # Referansı saklayın
                    image_label.pack(pady=10)


        # Kapat, Çıkış ve Karanlık Mod düğmelerini ekleyin
        karanlik_mod_dugme = ttk.Button(top_hotels_window, text="Dark Mode",command=karanlik_mod.karanlik_modunu_degistir)
        karanlik_mod_dugme.pack(side="bottom", pady=10)

        cikis_butonu = ttk.Button(top_hotels_window, text="Close Window", command=top_hotels_window.destroy)
        cikis_butonu.pack(side="bottom", pady=10)

        cikis_ana_butonu = ttk.Button(top_hotels_window, text="Exit", command=cikis_yap)
        cikis_ana_butonu.pack(side="bottom", pady=10)



    def geri_butonu_tiklandi():
        rezervasyon_pencere.withdraw()
        root.deiconify()

    contact_us_button = ttk.Button(rezervasyon_pencere, text="Contact Us", command=karanlik_mod.open_instagram)
    contact_us_button.pack(side="bottom", padx=10, pady=5)

    cikis_butonu_rezervasyon = ttk.Button(rezervasyon_pencere, text="Exit",command=rezervasyon_pencere.destroy)
    cikis_butonu_rezervasyon.pack(side="bottom", pady=5)

    geri_butonu = ttk.Button(rezervasyon_pencere, text="Back", command=geri_butonu_tiklandi)
    geri_butonu.pack(side="bottom", pady=5)

# Hoşgeldiniz metnini oluştur
hosgeldiniz_metni = tk.Label(root, text="Welcome to the Cheapest Hotel Finder Program", font=("Helvetica", 20, "bold"), pady=20)
hosgeldiniz_metni.pack()

# Karanlık modu özelliğini ekleyin
karanlik_mod = KaranlikMod(root)

# Giriş Butonu
giris_butonu = ttk.Button(root, text="Click Here to Make a Reservation", command=giris_tiklandi)
giris_butonu.pack(pady=20)

contact_us_button = ttk.Button(root, text="Contact Us", command=karanlik_mod.open_instagram)
contact_us_button.pack(side="bottom", padx=10, pady=10)

# Çıkış Butonu
cikis_butonu = ttk.Button(root, text="Exit", command=cikis_yap)
cikis_butonu.pack(side="bottom",pady=20)

root.mainloop()