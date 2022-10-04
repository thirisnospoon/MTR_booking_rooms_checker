from urllib.request import urlopen
from bs4 import BeautifulSoup

HOTEL_LIST_PATH = "../txt_data/hotels.txt"
OUTPUT_LOG_PATH = "../txt_data/ready_logs/breakfast_log.txt"

with open(HOTEL_LIST_PATH) as f:
    lines = f.readlines()
    counter = 1
    for line in lines:
        dataList = line.split(',')
        hotelName = dataList[0]
        mtrHotelURL = dataList[1].strip()
        bookingHotelURL = dataList[2].strip()
        try:
            bookingBreakfastList = BeautifulSoup(urlopen(bookingHotelURL), "html.parser") \
                .find('span', {'class': 'ph-item-copy-breakfast-option'}).text.strip().split(', ')

            mtrBreakfastTags = BeautifulSoup(urlopen(mtrHotelURL), "html.parser").find('strong',
                                                                                       string='Breafast info:').parent.find_next_sibling(
                'ul').find_all('li')
            mtrBreakfastList = []
            for option in mtrBreakfastTags:
                mtrBreakfastList.append(option.text.strip())

            if mtrBreakfastList == bookingBreakfastList:
                print(f'{counter}. {hotelName} \n'
                      f'Status: OK \n')
            else:
                print(f'{counter}. {hotelName} \n'
                      f'mtrURL: {mtrHotelURL} \n'
                      f'bookingURL: {bookingHotelURL}'
                      f'Status: FAIL \n'
                      f'MTR: {mtrBreakfastList} \n'
                      f'Booking {bookingBreakfastList}')

            with open(OUTPUT_LOG_PATH, "a") as file:
                if mtrBreakfastList == bookingBreakfastList:
                    file.write(f'{counter}. {hotelName} \n'
                               f'Status: OK \n')
                else:
                    file.write(f'{counter}. {hotelName} \n'
                               f'mtrURL: {mtrHotelURL} \n'
                               f'bookingURL: {bookingHotelURL}\n'
                               f'Status: FAIL \n'
                               f'MTR: {mtrBreakfastList} \n'
                               f'Booking {bookingBreakfastList}')
        except:
            print('no breakfast block')
            with open(OUTPUT_LOG_PATH, "a") as file:
                file.write(f'{counter}. {hotelName} \n'
                           f'mtrURL: {mtrHotelURL} \n'
                           f'bookingURL: {bookingHotelURL}'
                           f'Status: NO Breakfast Block \n')

        counter = counter + 1
