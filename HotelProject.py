import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar  # Takvim için

def giris_tiklandi():
    root.withdraw()  # Mevcut pencereyi gizle
    rezervasyon_ekrani()

def rezervasyon_ekrani():
    rezervasyon_pencere = tk.Toplevel()
    rezervasyon_pencere.title("Rezervasyon Ekranı")
    rezervasyon_pencere.geometry("800x900")  # Pencere boyutunu ayarla

    # Şehir Seçimi
    tk.Label(rezervasyon_pencere, text="Şehir Seçiniz:").pack()
    sehirler = ["Amsterdam", "Barcelona", "Berlin", "Lizbon", "Paris", "Prag", "Roma", "Venedik", "Viyana", "Zürih"]
    sehirler_listesi = tk.Listbox(rezervasyon_pencere, selectmode="single", height=len(sehirler))
    for sehir in sehirler:
        sehirler_listesi.insert(tk.END, sehir)
    sehirler_listesi.pack()

    # Giriş Tarihi Seçimi
    tk.Label(rezervasyon_pencere, text="Giriş Tarihi Seçiniz:").pack()
    g_tarihi = tk.StringVar()
    def g_tarih_sec():
        g_tarih = tk.Toplevel()
        cal = Calendar(g_tarih, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=20, pady=20)
        def g_tarih_onay():
            g_tarihi.set(cal.get_date())
            g_tarih.destroy()
        g_tarih_onay_button = tk.Button(g_tarih, text="Onayla", command=g_tarih_onay)
        g_tarih_onay_button.pack(pady=10)
    g_tarih_sec_button = tk.Button(rezervasyon_pencere, text='Giriş Tarihi Seç', command=g_tarih_sec)
    g_tarih_sec_button.pack()

    # Çıkış Tarihi Seçimi
    tk.Label(rezervasyon_pencere, text="Çıkış Tarihi Seçiniz:").pack()
    c_tarihi = tk.StringVar()
    def c_tarih_sec():
        c_tarih = tk.Toplevel()
        cal = Calendar(c_tarih, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=20, pady=20)
        def c_tarih_onay():
            c_tarihi.set(cal.get_date())
            c_tarih.destroy()
        c_tarih_onay_button = tk.Button(c_tarih, text="Onayla", command=c_tarih_onay)
        c_tarih_onay_button.pack(pady=10)
    c_tarih_sec_button = tk.Button(rezervasyon_pencere, text='Çıkış Tarihi Seç', command=c_tarih_sec)
    c_tarih_sec_button.pack()

    # Ödeme Şekli Seçimi
    tk.Label(rezervasyon_pencere, text="Ödeme Şekli Seçiniz:").pack()
    odeme_sekli = tk.StringVar()
    odeme_sekli.set("Euro")
    odeme_sekli_radio1 = tk.Radiobutton(rezervasyon_pencere, text="Euro", variable=odeme_sekli, value="Euro")
    odeme_sekli_radio1.pack()
    odeme_sekli_radio2 = tk.Radiobutton(rezervasyon_pencere, text="TL", variable=odeme_sekli, value="TL")
    odeme_sekli_radio2.pack()

    def onayla():
        secilen_sehir = sehirler_listesi.get(sehirler_listesi.curselection())
        giris_tarihi = g_tarihi.get()
        cikis_tarihi = c_tarihi.get()
        secilen_odeme_sekli = odeme_sekli.get()
        messagebox.showinfo("Rezervasyon Bilgileri",
                            f"Seçilen Şehir: {secilen_sehir}\n"
                            f"Giriş Tarihi: {giris_tarihi}\n"
                            f"Çıkış Tarihi: {cikis_tarihi}\n"
                            f"Ödeme Şekli: {secilen_odeme_sekli}")

    onay_butonu = tk.Button(rezervasyon_pencere, text="Onayla", command=onayla)
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
                         fg="Black" #font rengi
                         ,width=10,
                         height=2,
                         relief="raised", #flat=düz, raised=yukarı, sunken=aşağı
                         borderwidth=10,  # Kenar kalınlığı
                         padx=10, pady=10 # Düğme içindeki boşluk xy ekseni
                         )
giris_butonu.pack(pady=75)

# Pencereyi göster
root.mainloop()
