from urllib.request import urlopen
from bs4 import BeautifulSoup

HOTEL_LIST_PATH = "../txt_data/hotels.txt"
OUTPUT_LOG_PATH = "./test-logs/age-policy_log.txt"

with open(HOTEL_LIST_PATH) as f:
    lines = f.readlines()
    counter = 1
    allowedList = []
    for line in lines:
        dataList = line.split(',')
        hotelName = dataList[0]
        mtrHotelURL = dataList[1].strip()
        bookingHotelURL = dataList[2].strip()

        bookingAgePolicyText = BeautifulSoup(urlopen(bookingHotelURL), "html.parser") \
            .find('div', {'id': 'age_restriction_policy'}) \
            .text.strip() \
            .replace('\n', ' ') \
            .replace(' ', '') \
            .replace('-', '') \
            .lower()

        mtrAgePolicyTag = BeautifulSoup(urlopen(mtrHotelURL), "html.parser") \
            .find('table', {'class': 'st-properties'}) \
            .find_all('tr')[-1] \
            .find('td') \
            .find_all()
        mtrAgePolicyTitle = mtrAgePolicyTag[-4]
        mtrAgePolicyContent = mtrAgePolicyTag[-3]
        mtrAgePolicyText = (mtrAgePolicyTitle.text + mtrAgePolicyContent.text)\
            .strip()\
            .lower()\
            .replace(' ', '')\
            .replace('-', '')
        hotelReport = ''
        if bookingAgePolicyText == mtrAgePolicyText:
            hotelReport = f'{counter}. {hotelName}\n' \
                     f'Status: OK\n'
        else:
            hotelReport = f'{counter}. {hotelName}\n' \
                     f'{mtrHotelURL}\n' \
                     f'{bookingHotelURL}\n' \
                     f'mtrText: {mtrAgePolicyText}\n' \
                     f'bookingText: {bookingAgePolicyText}\n' \
                     f'Status: FAIL\n'
        with open(OUTPUT_LOG_PATH, "a") as file:
            file.write(hotelReport)
        print(hotelReport)

        counter = counter + 1
