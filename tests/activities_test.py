from urllib.request import urlopen
from bs4 import BeautifulSoup

HOTEL_LIST_PATH = "../txt_data/hotels.txt"
OUTPUT_LOG_PATH = "../txt_data/ready_logs/activities_log.txt"

with open(HOTEL_LIST_PATH) as f:
    lines = f.readlines()
    counter = 1
    failCounter = 0
    successCounter = 0
    for line in lines:
        dataList = line.split(',')
        hotelName = dataList[0]
        mtrHotelURL = dataList[1].strip()
        bookingHotelURL = dataList[2].strip()

        try:
            bookingActivitiesList = BeautifulSoup(urlopen(bookingHotelURL), "html.parser")\
                .find_all("span", {'class': "ph-item-copy-activity-unknown"})

            bookingActivitiesArray = []
            for activity in bookingActivitiesList:
                bookingActivitiesArray.append(activity.text.strip())

            mtrActivitiesList = BeautifulSoup(urlopen(mtrHotelURL), "html.parser")\
                .find('strong', string='Activities:')\
                .parent.find_next_sibling('ul')\
                .find_all('li')

            mtrActivitiesArray = []
            for activity in mtrActivitiesList:
                mtrActivitiesArray.append(activity.text.strip())

            if bookingActivitiesArray == mtrActivitiesArray:
                logText = f'{counter}. {hotelName}\n' \
                          f'Status: SUCCESS \n\n'
                with open(OUTPUT_LOG_PATH, "a") as file:
                    file.write(logText)
                    print(logText)
            else:
                logText = f'{counter}. {hotelName}\n' \
                          f'mtrURL: {mtrHotelURL}\n' \
                          f'bookingURL: {bookingHotelURL}\n' \
                          f'Status: FAIL\n' \
                          f'mtr Activities: {mtrActivitiesArray}\n' \
                          f'booking Activities: {bookingActivitiesArray}\n\n'
                with open(OUTPUT_LOG_PATH, "a") as file:
                    file.write(logText)
                    print(logText)
        except:
            logText = f'{counter}. {hotelName}\n' \
                      f'mtrURL: {mtrHotelURL}\n' \
                      f'bookingURL: {bookingHotelURL}\n' \
                      f'Status: NO ACTIVITIES BLOCK\n'
            with open(OUTPUT_LOG_PATH, "a") as file:
                file.write(logText)
                print(logText)

        counter = counter + 1
