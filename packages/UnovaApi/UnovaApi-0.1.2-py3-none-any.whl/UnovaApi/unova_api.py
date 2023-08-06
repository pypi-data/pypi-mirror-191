import time
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from UnovaApi import drawCaptchas
from UnovaApi.Exceptions import *
import csv
from bs4 import BeautifulSoup
import requests
from UnovaApi import unoSession
from twocaptcha import TwoCaptcha
import requests
import lxml
from importlib import resources
import io

key = "fd2d4f222211e317c6a77c7b02d69f78"
solver = TwoCaptcha(key)

options = Options()
options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])


def grab_team(page):
    try:
        team = page.find(class_="bt-pokemon-list").find_all('li')
    except AttributeError:
        return None

    poke_list = []
    for pokemon in team:
        name = pokemon.find('img')['title']
        level = pokemon.find('small').text
        image_url = pokemon.find('img')['src']

        data = {"name": name,
                "level": level,
                "sprite": image_url}
        poke_list.append(data)

    return poke_list


def shop():
    with resources.open_text("UnovaApi","item_data.csv") as f:
        file = csv.reader(f)
        return {row[1]: row[3] for row in file}


def adoption_center():
    with resources.open_text("UnovaApi", "adoption_data.csv") as f:
        file = csv.reader(f)
        return [row[1] for row in file]


class Client:
    def __init__(self, username: str, password: str):
        try:
            __sesh = unoSession.login(username, password)
        except LoginError as e:
            raise RuntimeError('Username or Password Incorrect! (Or all pokemon on your team have fainted)') from e
        self.__member_panel = __sesh[0]
        self.__cookies = __sesh[1]
        self.username = __sesh[2]

    def view_team(self, player=None):
        if not player:
            player = self.__member_panel
        else:
            player = self.__find_player(player)
        return grab_team(player)

    def __find_player(self, username):
        payload0 = [("xjxfun", "retrieveMembers"),
                    ("xjxargs[]", "N1"),
                    ("xjxargs[]", "Sid"),
                    ("xjxargs[]", f"S{username}")]

        with requests.Session() as session:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                player = session.post("https://www.unovarpg.com/search_trainer.php", data=payload0,
                                      cookies=self.__cookies)
                playerSoup = BeautifulSoup(player.content, 'lxml')
                try:
                    playerID = playerSoup.find('a')['href'].lstrip("battle.php?type=autotrainer&tid=")
                except TypeError:
                    return -1
                payload1 = {"xjxfun": "viewProfile",
                            "xjxargs[]": f"N{playerID}"}

                player_prof = session.post("https://www.unovarpg.com/search_trainer.php", data=payload1,
                                           cookies=self.__cookies)
                return BeautifulSoup(player_prof.content, 'lxml')

    def buy_item(self, itemName: str, item_quantity: int):

        with open("item_data.csv") as f:
            file = csv.reader(f)
            for row in file:
                if row[1].lower().startswith(itemName.lower()):
                    itemID = row[2]
                    itemPrice = row[3]
                    itemName = row[1]
        try:
            data = {f"item[{itemID}]": f'{item_quantity}'}
        except UnboundLocalError:
            print("Item Not Found")
            return 0
        with requests.Session() as session:
            purchase = session.post("https://www.unovarpg.com/shop.php?doBuy", cookies=self.__cookies, data=data)
            print(f"You purchased {item_quantity} {itemName} from the shop for {itemPrice} each!")
            self.__member_panel = BeautifulSoup(requests.get("https://www.unovarpg.com/member_panel.php",
                                                             cookies=self.__cookies).content, 'html.parser')

    def player_info(self, player=None):
        if player:
            player = self.__find_player(player)
        else:
            player = self.__find_player(self.username)

        if player == -1:
            return None
        tables = player.find_all(class_="memberPanelTable")
        member_panel_table = tables[0]
        ls = member_panel_table.text.strip().split("\n")
        ls.pop(1)
        out = {"Trainer Name": ls.pop(0)}
        ls.pop(4)
        for thing in ls:
            key, val = thing.split(':')
            out[key.strip()] = val.strip()
        out['Total captured pokemon'] = tables[2].find_all('span')[-1].text.lstrip("Total captured Pokemon: ")

        return out

    def heal_team(self):
        payload = {"xjxfun": "recoverMyPokemon"}
        requests.post("https://www.unovarpg.com/pokemon_center.php", data=payload, cookies=self.__cookies)
        requests.get("https://www.unovarpg.com/setup_team.php", cookies=self.__cookies)

        return "heal finished"

    def view_items(self):
        def stripp(i, item):
            return (item.text.strip().strip().split('x'))[i].strip()

        item_list = self.__member_panel.find(class_="item-list-dashboard").find_all('li')
        items = [{"name": stripp(0, item), "quantity": stripp(1, item)} for item in item_list]
        return items

    def add_friend(self, username):
        if self.__find_player(username) == -1:
            print("User not found")
            return
        else:
            payload = {"xjxfun": "addFriend",
                       "xjxargs[]": f"S{username}"}
            for i in range(2):
                requests.post("https://www.unovarpg.com/search_trainer.php", data=payload, cookies=self.__cookies)

    def send_money(self, username: str, quantity: float, captcha=0):
        if self.__find_player(username) == -1:
            print("User not found")
            return None
        if type(quantity) not in (int, float):
            raise TypeError('Quantity must be a numeric value')
        elif quantity < 100:
            print("Quantity must be >= 100")
            return 0
        amt_to_send = round((100 / 85) * quantity, 2)
        bal = self.check_balance()
        if amt_to_send > bal:
            print(f"Not enough money in your account\nYour balance: {bal}\nAmount to send (+tax): {amt_to_send}")
            return -1

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.unovarpg.com/notfound")
        sCookies = {}
        for item in self.__cookies.items():
            driver.add_cookie({"name": item[0], "value": item[1]})

        driver.get("https://www.unovarpg.com/indigo_bank.php")
        img = driver.find_element(by='xpath', value='//*[@id="basicContainer"]/div[3]/div[2]/form/img')

        print(f"Sending IC${quantity} to {username}\nPlease wait while we solve the captcha...")
        driver.execute_script("arguments[0].scrollIntoView();", img)
        with open("captcha.png", 'wb') as file:
            file.write(img.screenshot_as_png)
        if captcha:
            ans = solver.normal("captcha.png", minLen=5, maxLen=5)['code'].lower()
        else:
            drawCaptchas.draw_image("captcha.png", 40, 141)
            ans = input("Solve the Captcha: ")
        print(ans)
        print(f"Captcha Solved.\n{username} received IC${quantity} and you lost IC${amt_to_send} due to tax")
        payload = {
            "username": username,
            "quantity": amt_to_send,
            "captcha": ans
        }
        requests.post("https://www.unovarpg.com/indigo_bank.php?doTransaction", data=payload, cookies=self.__cookies)
        self.__member_panel = BeautifulSoup(requests.get("https://www.unovarpg.com/member_panel.php",
                                                         cookies=self.__cookies).content, 'html.parser')
        return amt_to_send

    def send_message(self, username: str, subject: str, message: str, captcha=0):
        if self.__find_player(username) == -1:
            print("User not found")
            return None

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.unovarpg.com/notfound")
        sCookies = {}
        for item in self.__cookies.items():
            driver.add_cookie({"name": item[0], "value": item[1]})

        driver.get("https://www.unovarpg.com/write_message.php")
        img = driver.find_element(by='xpath', value='//*[@id="basicContainer"]/div[3]/div[2]/form/img')

        print(f"Sending message to {username}\nPlease wait while we solve the captcha...")
        driver.execute_script("arguments[0].scrollIntoView();", img)
        with open("captcha.png", 'wb') as file:
            file.write(img.screenshot_as_png)
        if captcha:
            ans = solver.normal("captcha.png", minLen=5, maxLen=5)['code'].lower()
        else:
            drawCaptchas.draw_image("captcha.png", 40, 141)
            ans = input("Solve the Captcha: ")
        print(ans)
        if ans == 'subject':
            print("Captcha not solved. Please try again.")
            return
        print(f"Message Sent")
        payload = {
            "username": username,
            "subject": subject,
            "captcha": ans,
            "message": message
        }
        requests.post("https://www.unovarpg.com/write_message.php?doSend", data=payload, cookies=self.__cookies)

        return payload

    def check_balance(self):
        balance = self.__member_panel.find(class_="memberPanelTable").find('div').text.strip(). \
            split('\n')[5].lstrip("IC$: ")
        # print("IC$: "+balance)
        balance = balance.split(',')
        return int("".join(balance))

    def messages(self, index=-1, action='open'):
        payload = {'xjxfun': "retrieveMessages",
                   'xjxargs[]': "S1"}
        page = requests.post("https://www.unovarpg.com/member_panel.php", data=payload, cookies=self.__cookies)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            message_soup = BeautifulSoup(page.content, "lxml")
        message_list = message_soup.find_all('li')
        messages = []
        for msg in message_list:
            data = {"subject": msg.find(class_="title").text.title(),
                    "author": msg.find(class_="description").text.split("|")[0].strip(),
                    "date": msg.find(class_="description").text.split("|")[1].strip(),
                    "id": msg.find('a')['id'].lstrip("pm_")
                    }
            messages.append(data)

        if index == -1:
            print(f"You have {len(messages)} Messages")
            return len(messages)

        elif index > -1 and action == 'open':
            msg = messages[index]
            payload = {"xjxfun": "openMessage",
                       "xjxargs[]": "S" + msg['id']}
            content = requests.post("https://www.unovarpg.com/member_panel.php", data=payload, cookies=self.__cookies)
            msg_soup = BeautifulSoup(content.content, 'lxml')
            message = msg_soup.find('p').text.title()
            msg.pop("id")
            msg["message"] = message
            return msg

        elif index > -1 and action == 'delete':
            msg = messages[index]
            payload = {"xjxfun": "deleteMessage",
                       "xjxargs[]": "N" + msg['id']}
            requests.post("https://www.unovarpg.com/member_panel.php", cookies=self.__cookies, data=payload)
            time.sleep(.5)
            self.__member_panel = requests.get("https://www.unovarpg.com/member_panel.php", cookies=self.__cookies)
            return 1

    def adopt(self, pokemonName: str):

        with open("adoption_data.csv") as f:
            file = csv.reader(f)
            for row in file:
                if row[1].lower().startswith(pokemonName.lower()):
                    pkID = row[2]
                    pokemonName = row[1]
        try:
            data = {f"item[{pkID}]": '1'}
        except UnboundLocalError:
            print("Pokemon Not Found in Adoption Center")
            return None
        with requests.Session() as session:
            purchase = session.post("https://www.unovarpg.com/adoption_center.php?doBuy", cookies=self.__cookies,
                                    data=data)
            self.__member_panel = BeautifulSoup(requests.get("https://www.unovarpg.com/member_panel.php",
                                                             cookies=self.__cookies).content, 'lxml')

            return pokemonName

    def battle_team(self):
        payload = {
            "xjxfun": "getBattleTeam",
            "xjxargs[]": "Btrue"
        }

        page = requests.post("https://www.unovarpg.com/setup_team.php", data=payload, cookies=self.__cookies)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            team_soup = BeautifulSoup(page.content, 'lxml')

        pokemon_data = team_soup.find(class_="bt-pokemon-list")
        pokemon_list = pokemon_data.find_all("li")
        team = []
        # print(pokemon_list)
        for pokemon in pokemon_list:
            pkm = pokemon.find('a')['title'].lstrip("header=[").rstrip("]")
            actual_soup = BeautifulSoup(pkm, "html.parser")
            name, details = actual_soup.text.split("'s Details...] body=[")
            name = name.strip()
            details = details.strip()
            data = {
                "Name": name
            }

            for item in details.split("\n"):
                if "Att" in item:
                    moves, attached = item.split("Attached Item: ")
                    moves = moves.strip().split("Att. ")
                    moves.pop(0)

                    attached = attached.strip()

                    data.update({"Moves": moves,
                                 "Attached Item": attached})
                    pass
                else:
                    split = item.split(":")
                    key = split[0].strip()
                    value = split[1].strip()
                    data.update({key: value})
            team.append(data)

        return team
