from urllib.request import urlopen
from bs4 import BeautifulSoup

HOTEL_LIST_PATH = "../txt_data/hotels.txt"
OUTPUT_LOG_PATH = "./test-logs/check_policy_log.txt"

with open(HOTEL_LIST_PATH) as f:
    lines = f.readlines()
    counter = 1
    allowedList = []
    for line in lines:
        dataList = line.split(',')
        hotelName = dataList[0]
        mtrHotelURL = dataList[1].strip()
        bookingHotelURL = dataList[2].strip()

        # bookingCheckPolicyHtml = BeautifulSoup(urlopen(bookingHotelURL), "html.parser").find('div', {'id': "checkin_policy"})
        bookingCheckPolicylist = BeautifulSoup(urlopen(bookingHotelURL), "html.parser").find_all('span', {
            'class': 'u-display-block'})
        if len(bookingCheckPolicylist) == 3:
            bookingCheckPolicylist.pop(0)
        bookingCheckPolicyString = ''
        for e in bookingCheckPolicylist:
            bookingCheckPolicyString = bookingCheckPolicyString + e.text.strip() \
                .replace('\n', '') \
                .replace(' ', '') \
                .replace(':', '') \
                .replace('-', '') \
                .replace('From', '') \
                .replace('Until', '') \
                .replace('hours', '')

        mtrCheckInPolicyTag = BeautifulSoup(urlopen(mtrHotelURL), "html.parser") \
            .find('table', {'class': 'st-properties'}) \
            .find_all('tr')[0] \
            .find('td') \
            .text \
            .replace('\n', '') \
            .replace(' ', '') \
            .replace('00:00', '') \
            .replace(':', '') \
            .replace('-', '') \


        mtrCheckOutPolicyTag = BeautifulSoup(urlopen(mtrHotelURL), "html.parser") \
            .find('table', {'class': 'st-properties'}) \
            .find_all('tr')[1] \
            .find('td') \
            .text \
            .replace('\n', '') \
            .replace(' ', '') \
            .replace('00:00', '') \
            .replace(':', '') \
            .replace('-', '')

        mtrCheckPolicyString = mtrCheckInPolicyTag + mtrCheckOutPolicyTag

        hotelReport = ''

        if mtrCheckPolicyString == bookingCheckPolicyString:
            hotelReport = f'{counter}. {hotelName}\n' \
                     f'Status: OK\n'
        else:
            hotelReport = f'{counter}. {hotelName}\n' \
                     f'{mtrHotelURL}\n' \
                     f'{bookingHotelURL}\n' \
                     f'mtrText: {mtrCheckPolicyString}\n' \
                     f'bookingText: {bookingCheckPolicyString}\n' \
                     f'Status: FAIL\n'
        with open(OUTPUT_LOG_PATH, "a") as file:
            file.write(hotelReport)
        print(hotelReport)

        counter = counter + 1
