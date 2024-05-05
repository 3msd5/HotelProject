import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar  # Takvim için

class KaranlikMod:
    def __init__(self, root):
        self.root = root
        self.karanlik_mod = False

        # Karanlık modu aktif etme düğmesi
        self.karanlik_mod_dugme = tk.Button(root, text="Karanlık Mod", command=self.toggle_karanlik_mod, font=("Helvetica", 12))
        self.karanlik_mod_dugme.pack(side="bottom", pady=10)

    def toggle_karanlik_mod(self):
        # Karanlık modu açma veya kapatma işlemleri
        if not self.karanlik_mod:
            self.karanlik_mod = True
            self.root.config(bg="gray10")  # Arka plan rengini koyu gri yap
            self.karanlik_mod_dugme.config(bg="gray30", fg="white")  # Düğmenin arka plan ve yazı rengini değiştir
            self.apply_karanlik_mod(self.root)
        else:
            self.karanlik_mod = False
            self.root.config(bg="SystemButtonFace")  # Arka plan rengini varsayılan olarak geri getir
            self.karanlik_mod_dugme.config(bg="SystemButtonFace", fg="black")  # Düğmenin arka plan ve yazı rengini geri getir
            self.apply_normal_mod(self.root)

    def apply_karanlik_mod(self, widget):
        # Karanlık moda geçtiğimizde tüm widgetlarda renklerin değiştirilmesi
        if isinstance(widget, tk.Widget):
            widget.config(bg="gray20", fg="white")  # Arka plan rengini koyu gri, yazı rengini beyaz yap
        for child in widget.winfo_children():
            self.apply_karanlik_mod(child)

    def apply_normal_mod(self, widget):
        # Normal moda geçtiğimizde tüm widgetlarda renklerin geri getirilmesi
        if isinstance(widget, tk.Widget):
            widget.config(bg="SystemButtonFace", fg="black")  # Arka plan rengini varsayılana, yazı rengini siyaha geri getir
        for child in widget.winfo_children():
            self.apply_normal_mod(child)

secilen_sehir = ""  # secilen_sehir değişkenini global olarak tanımlayalım
giris_tarihi = ""
cikis_tarihi = ""

def giris_tiklandi():
    root.withdraw()  # Mevcut pencereyi gizle
    rezervasyon_ekrani()

def rezervasyon_ekrani():
    global secilen_sehir  # global değişkenleri tanımlayalım

    rezervasyon_pencere = tk.Toplevel()
    rezervasyon_pencere.title("Rezervasyon Ekranı")
    rezervasyon_pencere.geometry("800x900")  # Pencere boyutunu ayarla

    # Karanlık mod özelliğini ekleyelim
    karanlik_mod = KaranlikMod(rezervasyon_pencere)

    # Şehir Seçimi
    sehirler = ["Amsterdam", "Barcelona", "Berlin", "Lizbon", "Paris", "Prag", "Roma", "Venedik", "Viyana", "Zürih"]
    secilen_sehir = tk.StringVar(rezervasyon_pencere)
    secilen_sehir.set(sehirler[0])  # Başlangıçta ilk şehir seçili olacak
    sehirler_dropdown = tk.OptionMenu(rezervasyon_pencere, secilen_sehir, *sehirler)
    sehirler_dropdown.config(font=("Helvetica", 14))  # Font ayarlarını yap
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
    g_tarih_sec_button = tk.Button(rezervasyon_pencere, text='Giriş Tarihi Seç', command=g_tarih_sec, font=("Helvetica", 12))
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
                    messagebox.showerror("Hata", "Çıkış tarihi giriş tarihinden önce olamaz!")
                    return
            c_tarih_win.destroy()
        c_tarih_onay_button = tk.Button(c_tarih_win, text="Onayla", command=c_tarih_onay, font=("Helvetica", 12))
        c_tarih_onay_button.pack(pady=10)
    c_tarih_sec_button = tk.Button(rezervasyon_pencere, text='Çıkış Tarihi Seç', command=c_tarih_sec, font=("Helvetica", 12))
    c_tarih_sec_button.pack(pady=10)

    # Ödeme Şekli Seçimi
    tk.Label(rezervasyon_pencere, text="Ödeme Şekli Seçiniz:", font=("Helvetica", 14, "bold")).pack()
    odeme_sekli = tk.StringVar()
    odeme_sekli.set("Euro")
    odeme_sekli_radio1 = tk.Radiobutton(rezervasyon_pencere, text="Euro", variable=odeme_sekli, value="Euro", font=("Helvetica", 12))
    odeme_sekli_radio1.pack()
    odeme_sekli_radio2 = tk.Radiobutton(rezervasyon_pencere, text="TL", variable=odeme_sekli, value="TL", font=("Helvetica", 12))
    odeme_sekli_radio2.pack()

    # 1 Euro = 30 TL bilgisini ekleyelim
    tl_bilgisi_label = tk.Label(rezervasyon_pencere, text="1 Euro = 30 TL", font=("Helvetica", 10))
    tl_bilgisi_label.pack()

    def onayla():
        global secilen_sehir, giris_tarihi, cikis_tarihi  # onayla fonksiyonu içinde global değişkenleri kullanacağımızı belirtelim
        secilen_sehir = secilen_sehir.get()
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

    onay_butonu = tk.Button(rezervasyon_pencere, text="Onayla", command=onayla, font=("Helvetica", 12))
    onay_butonu.pack(pady=10)

# Ana uygulama penceresini oluştur
root = tk.Tk()
root.title("Otel Bulma")

# Pencere boyutunu ayarla
root.geometry("800x900")

hosgeldiniz_metni = tk.Label(root, text="Otel Bulma Programına Hoşgeldiniz",
                             font=("Helvetica", 25, "bold"),
                             fg="blue",justify="center")
hosgeldiniz_metni.pack(pady=50)

giris_butonu = tk.Button(root, text="Giriş", command=giris_tiklandi,
                         font=("Helvetica", 20, "bold"),
                         fg="Black",  # font rengi
                         width=10,
                         height=2,
                         relief="raised",  # flat=düz, raised=yukarı, sunken=aşağı
                         borderwidth=10,  # Kenar kalınlığı
                         padx=10, pady=10  # Düğme içindeki boşluk xy ekseni
                         )
giris_butonu.pack(pady=75)

# Karanlık mod özelliğini ana pencereye de ekleyelim
karanlik_mod = KaranlikMod(root)

# Pencereyi göster
root.mainloop()
