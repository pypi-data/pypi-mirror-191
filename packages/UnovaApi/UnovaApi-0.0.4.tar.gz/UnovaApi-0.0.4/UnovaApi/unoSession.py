import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
from UnovaApi.Exceptions import *


def login(username, password):
    page = requests.get("https://www.unovarpg.com/signin/?doLogin")
    cookies = page.cookies

    soup = BeautifulSoup(page.content, "html.parser")
    token = soup.find('form').find('input')['value']
    payload = {"username": username,
               "password": password,
               "unovarpg": token}

    with requests.Session() as session:
        member_panel = session.post("https://www.unovarpg.com/signin/?doLogin", data=payload, cookies=cookies)
        mem_soup = BeautifulSoup(member_panel.content, 'html.parser')
        try:
            user = mem_soup.find(class_="memberPanelTable").find('img')['title']
            print(f"Logged in as {user}")
            return mem_soup, cookies, user
        except AttributeError:
            raise LoginError


def __get_shop_items(username: str, password: str):
    sesh = login(username, password)
    mem_soup = sesh[0]
    cookies = sesh[1]

    with requests.Session() as session:
        items = []
        for i in range(1, 36):
            payload = {"xjxfun": "retrieveItems",
                       "xjxargs[]": f"S{i}",
                       }
            page = session.post("https://www.unovarpg.com/adoption_center.php", data=payload, cookies=cookies)
            shop_soup = BeautifulSoup(page.content, 'lxml')
            # print(shop_soup)
            for item in shop_soup.find_all(class_="shopItem"):
                # print(item)
                name = item.find(class_="item-name").text.strip()
                ID = item.find('input')['name'].strip('item')
                price = item.find('strong').text.strip(".-")

                items.append({"name": name,
                              "id": ID
                              })

        return pd.DataFrame(items)


# get_shop_items("alexRox", "alextif122").to_csv("adoption_data.csv")
