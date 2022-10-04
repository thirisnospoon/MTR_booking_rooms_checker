from bs4 import BeautifulSoup
from urllib.request import urlopen

HOTEL_LIST_PATH = "txt_data\\hotels.txt"
OUTPUT_LOG_PATH = "txt_data\\facilities-open-hours-log.txt"

with open(HOTEL_LIST_PATH) as f:
    lines = f.readlines()
    counter = 1
    openHoursHotelsCounter = 0
    openHoursList = []
    for line in lines:
        dataList = line.split(',')
        hotelName = dataList[0]
        mtrHotelURL = dataList[1].strip()
        bookingHotelURL = dataList[2].strip()

        bookingFacilitiesList = BeautifulSoup(urlopen(bookingHotelURL), "html.parser")\
            .find("div", {"class": "hotel-facilities__list"})\
            .find_all("div", {"class": "bui-spacer--large"})
        hasOpenHours = False
        for bookingFacility in bookingFacilitiesList:
            facilitiesGroupList = []
            bookingFacilityElements = bookingFacility \
                .find("div", {"class": "hotel-facilities-group"}) \
                .find_all("div", {"class": "bui-list__description"})
            for element in bookingFacilityElements:
                facilitiesGroupList.append(element
                                           .text
                                           .strip()
                                           .replace('\n\nAdditional charge', '')
                                           .replace('\n\nOff-site', ''))

            for element in facilitiesGroupList:
                if element == 'Opening times':
                    hasOpenHours = True
                    print('open hours found')
                    openHoursHotelsCounter = openHoursHotelsCounter + 1
                    break

            if hasOpenHours:
                openHoursList.append(bookingHotelURL)
                break

    print(f'Number of hotels found: {openHoursHotelsCounter}\n'
          f'url list:\n'
          f'{openHoursList}')