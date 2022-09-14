from bs4 import BeautifulSoup
from urllib.request import urlopen

with open("C:\\1\\linklist.txt", encoding="utf-8") as f:
    links = f.readlines()
    counter = 1
    for line in links:
        URL = line.strip() + ".en.html"
        soup = BeautifulSoup(urlopen(URL), "html.parser")

        hotelTitle = soup.find("h2", {"class": "pp-header__title"}).getText().strip()
        hotelAddress = soup.find("span", {"class": "hp_address_subtitle"}).getText().strip()
        hotelDescription = soup.find("div", {"id": "property_description_content"}).getText()
        importantInfoBigText = soup.find("div", {"class": "imporant_info_highlight"}).find("div", {
            "class": "description"}).getText

        facilitiesTagList = soup.find_all("div", {"class": "important_facility"})
        facilityList = []

        for facility in facilitiesTagList:
            facilityList.append(facility.getText().strip())

        activitiesTagList = soup.find_all("span", {"class": "ph-item-copy-activity-unknown"})
        activityList = []

        for activity in activitiesTagList:
            activityList.append(activity.getText().strip())

        try:
            with open("C:\\1\\hotelInfo.txt", "a") as file:
                file.write(hotelTitle + "\n" +
                           "URL: " + URL +
                           "\n\n\n")

            print(hotelTitle + " :  DONE!")
        except UnicodeEncodeError:
            print(hotelTitle + " going wrong")
