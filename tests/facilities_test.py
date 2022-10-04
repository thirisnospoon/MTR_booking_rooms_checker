from bs4 import BeautifulSoup
from urllib.request import urlopen

HOTEL_LIST_PATH = "../txt_data/hotels.txt"
OUTPUT_LOG_PATH = "../txt_data/facilities-log.txt"

with open(HOTEL_LIST_PATH) as f:
    lines = f.readlines()
    counter = 1
    for line in lines:
        dataList = line.split(',')
        hotelName = dataList[0]
        mtrHotelURL = dataList[1].strip()
        bookingHotelURL = dataList[2].strip()
        print(f'{counter}. {hotelName}\n'
              f'{mtrHotelURL}\n'
              f'{bookingHotelURL}\n')

        mtrFacilitiesGroups = BeautifulSoup(urlopen(mtrHotelURL), "html.parser") \
            .find("div", {"id": ["facilities-tab"]}) \
            .find_all("div", {"class": ["col-xs-6 col-sm-4"]})

        mtrFacilitiesDict = {}

        for group in mtrFacilitiesGroups:

            groupTitle = group.find("div", {"class": "new_f_block__head"}).text.strip()
            facilitiesGroupList = []

            facilityGroupElements = group \
                .find("ul", {"class": "new_f_block__body"}) \
                .find_all("li")

            for element in facilityGroupElements:
                facilitiesGroupList.append(element.text.strip())

            mtrFacilitiesDict[groupTitle] = facilitiesGroupList

        # del mtrFacilitiesDict['Most popular facilities']

        bookingFacilitiesList = BeautifulSoup(urlopen(bookingHotelURL), "html.parser") \
            .find("div", {"class": "hotel-facilities__list"}) \
            .find_all("div", {"class": "bui-spacer--large"})

        bookingFacilitiesDict = {}

        for bookingFacility in bookingFacilitiesList:

            groupTitle = bookingFacility \
                .find("div", {"class": "bui-title__text"}) \
                .text \
                .replace('\n', "")
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

            bookingFacilitiesDict[groupTitle] = facilitiesGroupList

        for key in mtrFacilitiesDict:
            mtrFacilitiesDict[key].sort()

        for key in bookingFacilitiesDict:
            bookingFacilitiesDict[key].sort()

        # print('MTR Dict\n' + str(mtrFacilitiesDict))
        # print('BOOKING Dict\n' + str(bookingFacilitiesDict))

        for key in bookingFacilitiesDict:
            if bookingFacilitiesDict[key] and key in mtrFacilitiesDict:
                if bookingFacilitiesDict[key] != mtrFacilitiesDict[key] and len(mtrFacilitiesDict[key]) != len(
                        bookingFacilitiesDict[key]):
                    print(key + ": FAIL, booking facilities count: " + str(
                        len(bookingFacilitiesDict[key])) + ", MTR facilities count: " + str(
                        len(mtrFacilitiesDict[key])))
                    with open(OUTPUT_LOG_PATH, "a") as file:
                        file.write(f'{str(counter)}. {hotelName.title()}\n'
                                   f'bookingHotelURL: {bookingHotelURL}\n'
                                   f'mtrHotelURL: {mtrHotelURL}\n')
                    with open(OUTPUT_LOG_PATH, "a") as file:
                        file.write((key + ": FAIL, booking facilities count: " + str(
                            len(bookingFacilitiesDict[key])) + ", MTR facilities count: " + str(
                            len(mtrFacilitiesDict[key])) + '\n'))
        counter = counter + 1
