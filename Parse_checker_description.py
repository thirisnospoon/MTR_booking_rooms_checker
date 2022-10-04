import time
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

HOTEL_LIST_PATH = "txt_data\\hotels.txt"
OUTPUT_LOG_PATH = "txt_data\\facilities-log.txt"

with open(HOTEL_LIST_PATH) as f:
    lines = f.readlines()
    counter = 1
    for line in lines:
        dataList = line.split(',')
        hotelName = dataList[0]
        mtrHotelURL = dataList[1].strip()
        bookingHotelURL = dataList[2].strip()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}
        result = requests.get(bookingHotelURL, headers=headers)
        c = result.content

        bookingSoup = BeautifulSoup(c, "html", )
        bookingMostPopularFacilitiesDivs = bookingSoup.find('div', {'class': 'hp_desc_important_facilities'}) \
            .find_all('div')

        print(bookingMostPopularFacilitiesDivs)
        bookingMostPopularFacilitiesList = []

        for element in bookingMostPopularFacilitiesDivs:
            bookingMostPopularFacilitiesList.append(element.text.strip())

        print(f"{hotelName}: {bookingMostPopularFacilitiesList}")
