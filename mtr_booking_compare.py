from bs4 import BeautifulSoup
from urllib.request import urlopen

HOTEL_LIST_PATH = "txt_data\\hotels.txt"
OUTPUT_LOG_PATH = "txt_data\\log.txt"

with open(HOTEL_LIST_PATH) as f:
    counter = 1
    failCounter = 0
    successCounter = 0

    lines = f.readlines()

    for line in lines:
        dataList = line.split(',')
        hotelName = dataList[0]
        mtrHotelURL = dataList[1].strip()
        bookingHotelURL = dataList[2].strip()

        mtrSoup = BeautifulSoup(urlopen(mtrHotelURL), "html.parser")
        bookingSoup = BeautifulSoup(urlopen(bookingHotelURL), "html.parser")

        mtrRoomBlocks = mtrSoup.find_all("a", {"class": ["st-link c-main"]})
        bookingRoomBlocks = bookingSoup.find_all("a", {"class": "js-legacy-room-name"})

        mtrRooms = []
        bookingRooms = []

        for mtrRoom in mtrRoomBlocks:
            mtrRooms.append(mtrRoom.getText())
        for bookingRoom in bookingRoomBlocks:
            bookingRooms.append(bookingRoom.getText())

        mtrRoomsNumber = len(mtrRooms)
        bookingRoomsNumber = len(bookingRooms)

        print(f'{str(counter)}. {hotelName.title()}\n'
              f'bookingHotelURL: {bookingHotelURL}\n'
              f'mtrHotelURL: {mtrHotelURL}\n'
              f'mtrRoomsNumber: {str(mtrRoomsNumber)}\n'
              f'bookingRoomsNumber: {str(bookingRoomsNumber)}')
        with open(OUTPUT_LOG_PATH, "a") as file:
            file.write(f'{str(counter)}. {hotelName.title()}\n'
                       f'bookingHotelURL: {bookingHotelURL}\n'
                       f'mtrHotelURL: {mtrHotelURL}\n'
                       f'mtrRoomsNumber: {str(mtrRoomsNumber)}\n'
                       f'bookingRoomsNumber: {str(bookingRoomsNumber)}\n')

        if bookingRoomsNumber > mtrRoomsNumber:
            print(f'rooms missed: {str(bookingRoomsNumber - mtrRoomsNumber)}\n'
                  f'Booking rooms: {str(bookingRooms)}\n'
                  f'mtr rooms: {str(mtrRooms)}\n'
                  f'status: FAILED\n\n')
            with open(OUTPUT_LOG_PATH, "a") as file:
                file.write(f'rooms missed: {str(bookingRoomsNumber - mtrRoomsNumber)}\n'
                           f'Booking rooms: {str(bookingRooms)}\n'
                           f'mtr rooms: {str(mtrRooms)}\n'
                           f'status: FAILED\n\n')
            failCounter = failCounter + 1
        elif bookingRoomsNumber < mtrRoomsNumber:
            print(f'extra rooms found: {str(mtrRoomsNumber - bookingRoomsNumber)}\n'
                  f'booking rooms: {str(bookingRooms)}\n'
                  f'mtr rooms: {str(mtrRooms)}\n'
                  f'status: FAILED\n\n')
            with open(OUTPUT_LOG_PATH, "a") as file:
                file.write(f'extra rooms found: {str(mtrRoomsNumber - bookingRoomsNumber)}\n'
                           f'booking rooms: {str(bookingRooms)}\n'
                           f'mtr rooms: {str(mtrRooms)}\n'
                           f'status: FAILED\n\n')
            failCounter = failCounter + 1
        else:
            print("Status: SUCCESS\n\n")
            with open(OUTPUT_LOG_PATH, "a") as file:
                file.write("Status: SUCCESS\n\n")
            successCounter = successCounter + 1
        counter = counter + 1

    print(f'success: {str(successCounter)} \n failed: {str(failCounter)}')

    with open(OUTPUT_LOG_PATH, "a") as file:
        file.write(f'\n----------------------------------------\n'
                   f'success: {str(successCounter)}\n'
                   f'failed: {str(failCounter)}\n')
