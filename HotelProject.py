import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests


class HotelListingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Best Hotels for You")

        self.create_gui()

    def create_gui(self):
        # City selection dropdown
        cities_label = ttk.Label(self.root, text="Select a city:")
        cities_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        cities = ["İzmir", "İstanbul", "Ankara", "Konya", "Hakkari"]  # Add more cities here
        self.city_dropdown = ttk.Combobox(self.root, values=cities, state="readonly")
        self.city_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Check-in date entry
        checkin_label = ttk.Label(self.root, text="Check-in date:")
        checkin_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.checkin_entry = ttk.Entry(self.root)
        self.checkin_entry.grid(row=1, column=1, padx=10, pady=10)

        # Check-out date entry
        checkout_label = ttk.Label(self.root, text="Check-out date:")
        checkout_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.checkout_entry = ttk.Entry(self.root)
        self.checkout_entry.grid(row=2, column=1, padx=10, pady=10)

        # Currency selection
        currency_label = ttk.Label(self.root, text="Select currency:")
        currency_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.currency_var = tk.StringVar(value="Euro")
        euro_radio = ttk.Radiobutton(self.root, text="Euro", variable=self.currency_var, value="Euro")
        euro_radio.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        tl_radio = ttk.Radiobutton(self.root, text="TL", variable=self.currency_var, value="TL")
        tl_radio.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        # Search button
        search_button = ttk.Button(self.root, text="Search", command=self.search_hotels)
        search_button.grid(row=4, columnspan=2, padx=10, pady=10)

    def search_hotels(self):
        selected_city = self.city_dropdown.get()
        checkin_date = self.checkin_entry.get()
        checkout_date = self.checkout_entry.get()
        currency = self.currency_var.get()

        # Booking.com'dan otel verilerini çekme kodu
        base_url = 'https://www.booking.com/searchresults.html?'
        params = {
            'ss': selected_city,
            'checkin': checkin_date,
            'checkout': checkout_date,
            'group_adults': '2',
            'no_rooms': '1',
            'group_children': '0'
        }
        url = base_url + '&'.join([f"{key}={value}" for key, value in params.items()])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # HTTP hata kontrolü
            soup = BeautifulSoup(response.text, 'html.parser')

            # Otel bilgilerini çıkarma
            hotel_elements = soup.select('div[data-testid="property-card"]')[:10]  # İlk 10 otel
            for hotel_element in hotel_elements:
                name = hotel_element.find('span', {'class': 'sr-hotel__name'}).text.strip()
                address = hotel_element.find('span', {'class': 'sr_card_address_line'}).text.strip()
                distance = hotel_element.find('span', {'data-testid': 'property-card-attribute-distance'}).text.strip()
                rating = hotel_element.find('span', {'class': 'bui-review-score__badge'}).text.strip()
                price = hotel_element.find('div', {'class': 'bui-price-display__value'}).text.strip()
                print(hotel_element.prettify())
                # TL ise Euro'ya dönüştür
                if currency == "TL":
                    price = f"{int(price.replace('₺', '').replace('.', '')) / 30:.2f} €"
                messagebox.showinfo("Hotel Info",
                                    f"Name: {name}\nAddress: {address}\nDistance: {distance}\nRating: {rating}\nPrice: {price}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


root = tk.Tk()
app = HotelListingApp(root)
root.mainloop()
