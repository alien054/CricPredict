# address : https://www.cricbuzz.com/profiles/

from time import sleep
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H_%M_%S")

player = {"id": "", "born": "", "name": "", "country": "", "role": "",
          "batting_style": "", "bowling_style": "", "bowling_hand": "", "bowling_type": ""}


#TODO: Soumma READ THIS
# choose values in pair; like if we choose start = 5000 it must be end = 10000
# run this code 4 times each time choosing one of the start end pair
# you will get the csv named as played_data_<start>_<end>_<current_time>.csv
# so each time you run you will get a new csv with out the chance of overwriting anything
# keep the csv that has run without interruption or exit successfully
# keep 4 such csv's that has the complete data

# TODO: Soumma change here
start = 0   # values should be 0     5000    10000    15000
end = 5000  # values should be 5000  10000   15000   20000


csv_file = open('playerData_'+str(start)+"_"+str(end)+"_" +
                current_time+'.csv', 'w', newline='')
fieldnames = list(player.keys())
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()

search_URL = "https://www.cricbuzz.com/profiles/"

print("Srcaping Data....")
# total_players = 20000


def progress(percent, width=40):
    left = (width * percent) // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%', sep='', end='', flush=True)


for i in range(start, end):
    print("{i}/{}".format(end-start))
    response = requests.get(search_URL+str(i))
    result_page = BeautifulSoup(response.content, 'html5lib')

    name = result_page.find('h1', attrs={"itemprop": "name"})

    if name != None and name.string != None:
        name = str(name.string).lower().strip()
        player["id"] = i
        player["name"] = name

        country = result_page.find(
            'h3', attrs={'class': 'cb-font-18 text-gray'}).string
        country = str(country).lower().strip()
        player["country"] = country

        player_info = result_page.find(
            'div', attrs={'class': 'cb-col cb-col-33 text-black'})
        for child in player_info.div.children:
            if "role" in str(child.string).lower():
                role = str(
                    child.next_sibling.next_sibling.string).lower().strip()
                player["role"] = role

            elif "born" in str(child.string).lower():
                try:
                    born = str(child.next_sibling.next_sibling.string).lower(
                    ).strip().split(" ")[2]
                    player["born"] = born
                except:
                    player["born"] = ""

            elif "batting style" in str(child.string).lower():
                batting_style = str(
                    child.next_sibling.next_sibling.string).lower().strip()
                player["batting_style"] = batting_style

            elif "bowling style" in str(child.string).lower():
                bowling_style = str(
                    child.next_sibling.next_sibling.string).strip().lower()
                bowling_hand = bowling_style.split(" ")[0]
                bowling_type = bowling_style.split(" ")[1]
                player["bowling_style"] = bowling_style
                player["bowling_hand"] = bowling_hand
                player["bowling_type"] = bowling_type

        # print(player)
        writer.writerow(player)

    # progress((i*100)//total_players)

print("\nSuccess!!!")
