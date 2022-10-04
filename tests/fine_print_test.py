import time

from bs4 import BeautifulSoup
from urllib.request import urlopen

HOTEL_LIST_PATH = "../txt_data/hotels.txt"
OUTPUT_LOG_PATH = "./test-logs/fine-print-log.txt"

with open(HOTEL_LIST_PATH) as f:
    lines = f.readlines()
    counter = 1
    emptyRestaurantsList = []
    failCounter = 0
    successCounter = 0
    failHotelsList = []

    for line in lines:
        dataList = line.split(',')
        hotelName = dataList[0]
        mtrHotelURL = dataList[1].strip()
        bookingHotelURL = dataList[2].strip()

        bookingFinePrintText = BeautifulSoup(urlopen(bookingHotelURL), "html.parser") \
            .find("div", {"id": "hp_important_info_box"}) \
            .find("div", {"class": "description"}).text \
            .strip() \
            .lower() \
            .replace('\n', '') \
            .replace(' ', '') \
            .replace(',', '') \
            .replace('/', '') \
            .replace(':', '') \
            .replace('.', '')

        mtrFinePrintText = BeautifulSoup(urlopen(mtrHotelURL), "html.parser") \
            .find('div', {'id': 'expert-tab'}) \
            .text \
            .strip() \
            .lower() \
            .replace('\n', '') \
            .replace(' ', '') \
            .replace(',', '') \
            .replace('/', '') \
            .replace(':', '') \
            .replace('.', '')

        if mtrFinePrintText == bookingFinePrintText:
            successCounter = successCounter + 1
            hotelReport = f'{counter}. {hotelName}\n' \
                          f'Status: SUCCESS\n\n'
            print(hotelReport)
            with open(OUTPUT_LOG_PATH, "a") as file:
                file.write(hotelReport)
        else:
            failCounter = failCounter + 1
            failHotelsList.append(counter)
            hotelReport = f'{counter}. {hotelName}\n' \
                          f'Status: FAIL\n' \
                          f'bookingURL: {bookingHotelURL}\n' \
                          f'mtrURL: {mtrHotelURL}\n' \
                          f'bookingString:\n' \
                          f'{bookingFinePrintText}\n' \
                          f'mtrString:\n' \
                          f'{mtrFinePrintText}\n\n'
            with open(OUTPUT_LOG_PATH, "a") as file:
                file.write(hotelReport)
            print(hotelReport)
        counter = counter + 1

    finalReport = f'SUCCESS count: {successCounter}\n' \
                  f'FAIL count: {failCounter}\n' \
                  f'Failed hotels: {failHotelsList}\n'
    with open(OUTPUT_LOG_PATH, "a") as file:
        file.write(finalReport)
    print(finalReport)
