from urllib.request import urlopen
from bs4 import BeautifulSoup

HOTEL_LIST_PATH = "txt_data\\hotels.txt"
OUTPUT_LOG_PATH = "txt_data/banners_log.txt"

with open(HOTEL_LIST_PATH) as f:
    lines = f.readlines()
    counter = 1
    for line in lines:
        dataList = line.split(',')
        hotelName = dataList[0]
        mtrHotelURL = dataList[1].strip()
        bookingHotelURL = dataList[2].strip()

        sustainableBanner = BeautifulSoup(urlopen(bookingHotelURL), "html.parser")\
            .find('div', {'class': 'k2-hp--sustainability_banner'}).text
        healthBanner = BeautifulSoup(urlopen(bookingHotelURL), "html.parser") \
            .find('div', {'class': 'k2-hp--health_safety'}).text
        print(str(counter) + ". " + hotelName + "\n" + bookingHotelURL + "\nTravel Sustainable info:\n" + sustainableBanner)
        print("Health info:" + healthBanner)
        with open(OUTPUT_LOG_PATH, "a") as file:
            file.write(str(counter) + ". " + hotelName + "\n" + bookingHotelURL + "\n" + mtrHotelURL + "\nTravel Sustainable info:\n" + sustainableBanner)
            file.write("Health info:" + healthBanner)

        counter = counter + 1