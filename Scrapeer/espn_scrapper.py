# address : https://www.espncricinfo.com/ci/content/player/index.html
# player info : http://search.espncricinfo.com/

import requests
from bs4 import BeautifulSoup


def get_info(player_name: str):
    search_URL = "http://search.espncricinfo.com/ci/content/player/search.html?search="
    info_URL = "http://search.espncricinfo.com/"
    player_info = {"Playing role": "",
                   "Batting style": "", "Bowling style": ""}

    response = requests.get(search_URL+player_name)
    serach_page = BeautifulSoup(response.content, 'html5lib')

    player_unique_tag = serach_page.find('a', attrs={'class': "ColumnistSmry"})

    if player_unique_tag == None or len(player_unique_tag) != 1:
        return player_info

    player_url = player_unique_tag['href']

    response = requests.get(info_URL+player_url)
    player_page = BeautifulSoup(response.content, 'html5lib')

    player_details = player_page.findAll(
        'p', attrs={"class": "ciPlayerinformationtxt"})

    for info in player_details:
        if "Playing role" in info.b or "Batting style" in info.b or "Bowling style" in info.b:
            # print(f"{info.b.string}: {info.span.string}")
            player_info[info.b.string] = info.span.string
    return player_info
