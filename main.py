
import sys
import os

import requests
from requests import ReadTimeout
from requests import HTTPError
from requests import Timeout
from requests import ConnectionError

from random import uniform
from time import sleep

from deta import Deta
from bs4 import BeautifulSoup

from dotenv import load_dotenv


load_dotenv()

DOMAIN = os.environ['DOMAIN']
URL = os.environ['URL']
PROTOCOL = os.environ['PROTOCOL']
SECRET = os.environ['SECRET']
PROXIES = {f"{PROTOCOL}": f"{SECRET}"}
db = Deta(os.environ['KEY']).Base(os.environ['NAME_DB'])

user_agent = {}


def connect_via_proxy() -> str:
    while True:
        try:
            response = requests.get(
                URL,
                headers={'User-Agent': ''},
                proxies=PROXIES,
                timeout=6)
            return response.text
        except (ConnectionError, HTTPError, ReadTimeout, Timeout):
            sleep(uniform(60, 360))
            continue


def get_links(response: str) -> list:
    soup = BeautifulSoup(response, 'lxml')
    links = soup.find_all('a', "personLink")
    return [''.join((DOMAIN, link.get('href'))) for link in links]


def safe(list: list) -> None:
    for obj in list:
        sleep(0.01)
        db.put({'url':  obj}, key=obj)


def main():
    response = connect_via_proxy()
    list = get_links(response)
    safe(list)
    sys.exit()


if __name__ == '__main__':
    main()