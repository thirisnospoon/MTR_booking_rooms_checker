from bs4 import BeautifulSoup
from urllib.request import urlopen

HOTEL_LIST_PATH = "../txt_data/hotels.txt"
OUTPUT_LOG_PATH = "../txt_data/restaurants-log.txt"

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

        bookingRestaurantString = ''
        try:
            bookingRestaurantBlocks = BeautifulSoup(urlopen(bookingHotelURL), "html.parser") \
                .find("div", {"class": "restaurant-grid"}) \
                .find_all("div", {"class": "restaurant-block"})

            for restaurant in bookingRestaurantBlocks:
                bookingRestaurantString = bookingRestaurantString + restaurant \
                    .text \
                    .strip() \
                    .lower() \
                    .replace('\n', '') \
                    .replace(' ', '') \
                    .replace(',', '') \
                    .replace('/', '') \
                    .replace(':', '')
        except:
            pass

        mtrRestaurantString = BeautifulSoup(urlopen(mtrHotelURL), "html.parser") \
            .find("div", {"id": "resturans-tab"}) \
            .text.strip() \
            .lower() \
            .replace('\n', '') \
            .replace(' ', '') \
            .replace('/', '') \
            .replace(',', '') \
            .replace(':', '')

        if bookingRestaurantString == 0:
            emptyRestaurantsList.append(bookingHotelURL)

        if bookingRestaurantString == mtrRestaurantString:
            print(f'{counter}. {hotelName}\n'
                  f'Status: SUCCESS\n\n')
            with open(OUTPUT_LOG_PATH, "a") as file:
                file.write(f'{counter}. {hotelName}\n'
                           f'Status: SUCCESS\n\n')
            successCounter = successCounter + 1
        else:
            print(f'{counter}. {hotelName}\n'
                  f'Status: FAIL\n'
                  f'bookingURL: {bookingHotelURL}\n'
                  f'mtrURL: {mtrHotelURL}\n'
                  f'bookingString:\n'
                  f'{bookingRestaurantString}\n'
                  f'mtrString:\n'
                  f'{mtrRestaurantString}\n\n')
            with open(OUTPUT_LOG_PATH, "a") as file:
                file.write(f'{counter}. {hotelName}\n'
                           f'Status: FAIL\n'
                           f'bookingURL: {bookingHotelURL}\n'
                           f'mtrURL: {mtrHotelURL}\n'
                           f'bookingString:\n'
                           f'{bookingRestaurantString}\n'
                           f'mtrString:\n'
                           f'{mtrRestaurantString}\n\n')
            failCounter = failCounter + 1
            failHotelsList.append(counter)
        counter = counter + 1

    print(f'SUCCESS Hotels count: {successCounter}\n'
          f'FAIL Hotels count: {failCounter}\n'
          f'Failed hotels: {failHotelsList}\n'
          f'\n'
          f'Hotels without restaurants block on Booking.com:\n'
          f'{emptyRestaurantsList}')
    with open(OUTPUT_LOG_PATH, "a") as file:
        file.write(f'SUCCESS Hotels count: {successCounter}\n'
                   f'FAIL Hotels count: {failCounter}\n'
                   f'Failed hotels: {failHotelsList}\n'
                   f'\n')
