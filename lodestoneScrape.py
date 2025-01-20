# Scraps the lodestone page of a character and returns the image link of the character
import requests
from bs4 import BeautifulSoup


def get_character_image(lodestone_id:int):
    url = f"https://na.finalfantasyxiv.com/lodestone/character/{lodestone_id}/"
    responses = requests.get(url)

    soup = BeautifulSoup(responses.text, 'html.parser')

    img_tags = soup.find_all('img')
    target_div = soup.find('div', class_='frame__chara__face')

    img_link = target_div.find('img').attrs['src']
    return img_link