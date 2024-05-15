import tkinter as tk # gui
from tkinter import ttk, messagebox #uyarı mesajları
from tkcalendar import Calendar  # Tarih seçimi için
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from PIL import Image, ImageTk  # resimler için
import io

# Ana uygulama penceresini oluştur
root = tk.Tk()
root.title("Otel Bulma")
root.geometry("800x600")
# Stil oluştur
style = ttk.Style()
#style.theme_use('clam')  # Mevcut temayı kullanabilirsiniz

# Radyo butonlarının arka plan rengini değiştir

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
        current_date = now.strftime("%y-%m-%d")
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

    def on_sehir_sec(*args):      # Şehir seçimi değiştiğinde çağrılacak işlev
        global secilen_sehir
        secilen_sehir = sehirler_dropdown.get()

    # Şehir seçimi bileşenine işlevi bağlayın
    sehirler_dropdown.bind("<<ComboboxSelected>>", on_sehir_sec)

    # Giriş Tarihi Seçimi
    tk.Label(rezervasyon_pencere, text="Giriş Tarihi Seçiniz:", font=("Helvetica", 14, "bold")).pack()
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
        cal = Calendar(c_tarih_win, selectmode='day', date_pattern='yyyy-mm-dd')
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
    odeme_sekli_radio1 = ttk.Radiobutton(rezervasyon_pencere, text="€ - EURO", variable=odeme_sekli, value="EUR", style='TButton')
    odeme_sekli_radio1.pack()
    odeme_sekli_radio2 = ttk.Radiobutton(rezervasyon_pencere, text="₺ - TL", variable=odeme_sekli, value="TRY", style='TButton')
    odeme_sekli_radio2.pack()

    # 1 Euro = 30 TL bilgisini ekleyelim
    tl_bilgisi_label = tk.Label(rezervasyon_pencere, text="*1 Euro = 30 TL", font=("Helvetica", 10))
    tl_bilgisi_label.pack()

    def check_inputs():
        global giris_tarihi, cikis_tarihi
        if not giris_tarihi or not cikis_tarihi:
            messagebox.showerror("Hata", "Lütfen giriş ve çıkış tarihlerini seçin!")
            return False
        elif not odeme_sekli.get():
            messagebox.showerror("Hata", "Lütfen ödeme şeklini seçin!")
            return False
        elif cikis_tarihi <= giris_tarihi:
            messagebox.showerror("Hata", "Çıkış tarihi giriş tarihinden önce veya aynı olamaz!")
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
                            )
        # Otel verilerini göster
        show_hotels()

    onay_butonu = ttk.Button(rezervasyon_pencere, text="Onayla", command=onayla)
    onay_butonu.pack(pady=10)

    def scrape_hotels(city, checkin, checkout):
        try:
            print("Checkin:", checkin)
            print("Checkout:", checkout)
            print("Payment Type:", odeme_sekli.get())
            # Function to scrape hotel data from Booking.com
            base_url = "https://www.booking.com/searchresults.en-gb.html"
            query_params = {
            'label': 'gen173nr-1FCAEoggI46AdIM1gEaOQBiAEBmAEouAEHyAEM2AEB6AEB-AELiAIBqAIDuAKmksuxBsACAdICJDkwMzNiODdlLTdmYjYtNGMxMy1hYWZjLWI5NDM5NGI3MzdhN9gCBuACAQ',
            'sid': '75e30209011abe1aa1c492edf1647de4',
            'sb': '1',
            'sb_lp': '1',
            'src': 'index',
            'src_elem': 'sb',
            'error_url': 'https://www.booking.com/index.en-gb.html',
            'ss': city,
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
            url4 = f"https://www.booking.com/searchresults.en-gb.html?ss={city}&ssne={city}&ssne_untouched={city}&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaOQBiAEBmAEouAEHyAEM2AEB6AEB-AELiAIBqAIDuAKmksuxBsACAdICJDkwMzNiODdlLTdmYjYtNGMxMy1hYWZjLWI5NDM5NGI3MzdhN9gCBuACAQ&sid=75e30209011abe1aa1c492edf1647de4&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-2140479&dest_type=city&checkin={checkin}&checkout={checkout}&group_adults=2&no_rooms=1&group_children=0"
            url3 = f"https://www.booking.com/searchresults.en-gb.html?ss=Amsterdam&ssne=Amsterdam&ssne_untouched=Amsterdam&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaOQBiAEBmAEouAEHyAEM2AEB6AEB-AELiAIBqAIDuAKmksuxBsACAdICJDkwMzNiODdlLTdmYjYtNGMxMy1hYWZjLWI5NDM5NGI3MzdhN9gCBuACAQ&sid=75e30209011abe1aa1c492edf1647de4&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-2140479&dest_type=city&checkin=2024-05-14&checkout=2024-05-16&group_adults=2&no_rooms=1&group_children=0"
            url = f"https://www.booking.com/searchresults.en-gb.html?ss=Amsterdam&ssne=Amsterdam&ssne_untouched=Amsterdam&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaOQBiAEBmAEouAEHyAEM2AEB6AEB-AELiAIBqAIDuAKmksuxBsACAdICJDkwMzNiODdlLTdmYjYtNGMxMy1hYWZjLWI5NDM5NGI3MzdhN9gCBuACAQ&sid=75e30209011abe1aa1c492edf1647de4&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-2140479&dest_type=city&checkin={checkin}&checkout={checkout}&group_adults=2&no_rooms=1&group_children=0&selected_currency=EUR"
            print(checkout)
            print(checkin)
            print(url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.9'
            }
            response = requests.get(url, headers=headers)

            response.raise_for_status()  # Raises an exception for 4XX or 5XX status codes
            soup = BeautifulSoup(response.text, 'html.parser')
            hotels_data = []

            for hotel in soup.findAll('div', {'data-testid': 'property-card'}):
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

            return hotels_data

        except requests.RequestException as e:
            messagebox.showerror("Hata", f"İnternet bağlantısında bir sorun oluştu: {str(e)}")
            return []

    def show_hotels():
        city = secilen_sehir
        checkin = giris_tarihi
        checkout = cikis_tarihi

        hotels_data = scrape_hotels(city, checkin, checkout)
        if not hotels_data:
            messagebox.showerror("Hata", "Veri bulunamadı. Lütfen farklı bir tarih veya şehir seçin veya internet bağlantınızı kontrol edin.")
            return

        # Otelleri TXT dosyasına kaydet
        with open('myhotels.txt', 'w', encoding='utf-8') as txtfile:
            for hotel in hotels_data:
                txtfile.write(f"Otel Adı: {hotel['Hotel Title']}\n")
                txtfile.write(f"Adres: {hotel['Hotel Address']}\n")
                txtfile.write(f"Mesafe: {hotel['Distance to City Center']}\n")
                txtfile.write(f"Puan: {hotel['Hotel Rating']}\n")
                txtfile.write(f"Fiyat: {hotel['Price']}\n\n")

            # En iyi 5 otelleri göstermek için yeni pencere oluştur
        display_top_hotels_window(hotels_data)

    def display_top_hotels_window(top_hotels):
        top_hotels_window = tk.Toplevel()
        top_hotels_window.title("En Ucuz 5 Otel:")
        top_hotels_window.geometry("800x1000")

        top_hotels_frame = tk.Frame(top_hotels_window)
        top_hotels_frame.pack(pady=20)

        top_hotels_label = tk.Label(top_hotels_frame, text="En Ucuz 5 Otel:", font=("Helvetica", 16, "bold"))
        top_hotels_label.pack()

        # Resim alanı oluştur
        image_frame = tk.Frame(top_hotels_frame)
        image_frame.pack(side="left", fill="both", expand=True)
        # Metin alanı oluştur
        top_hotels_text = tk.Text(top_hotels_frame, height=36, width=100, font=("Helvetica", 12))
        top_hotels_text.pack(side="left", fill="both", expand=True)


        for hotel_index in range(5):  # Sadece ilk 5 oteli listele
            if hotel_index < len(top_hotels):
                hotel = top_hotels[hotel_index]

                top_hotels_text.insert(tk.END, f"\n\n\n\n************** {hotel_index + 1}. Otel **************\n"
                                               f"Otel Adı: {hotel['Hotel Title']}\n"
                                               f"Adres: {hotel['Hotel Address']}\n"
                                               f"Mesafe: {hotel['Distance to City Center']}\n"
                                               f"Puan: {hotel['Hotel Rating']}\n"
                                               f"Fiyat: {hotel['Price']}\n\n\n")
                # Otel resimlerini yükle ve göster
                if hotel['Image URL']:
                    response = requests.get(hotel['Image URL'])
                    image_data = response.content
                    image = Image.open(io.BytesIO(image_data))
                    image = image.resize((200, 200),Image.Resampling.LANCZOS)  # ANTIALIAS yerine Image.Resampling.LANCZOS kullan
                    photo = ImageTk.PhotoImage(image)

                    image_label = tk.Label(image_frame, image=photo)
                    image_label.image = photo  # Referansı saklayın
                    image_label.pack(pady=10)

        # Kapat, Çıkış ve Karanlık Mod düğmelerini ekleyin
        cikis_butonu = ttk.Button(top_hotels_window, text="Pencereyi Kapat", command=top_hotels_window.destroy)
        cikis_butonu.pack(side="bottom", pady=10)

        cikis_ana_butonu = ttk.Button(top_hotels_window, text="Çıkış", command=cikis_yap)
        cikis_ana_butonu.pack(side="bottom", pady=10)

        karanlik_mod_dugme = ttk.Button(top_hotels_window, text="Karanlık Mod",
                                        command=karanlik_mod.karanlik_modunu_degistir)
        karanlik_mod_dugme.pack(side="bottom", pady=10)

    def geri_butonu_tiklandi():
        rezervasyon_pencere.withdraw()
        root.deiconify()

    geri_butonu = ttk.Button(rezervasyon_pencere, text="Geri", command=geri_butonu_tiklandi)

    geri_butonu.pack(side="bottom", pady=10)

    cikis_butonu_rezervasyon = ttk.Button(rezervasyon_pencere, text="Çıkış",command=rezervasyon_pencere.destroy)
    cikis_butonu_rezervasyon.pack(side="bottom", pady=10)

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

