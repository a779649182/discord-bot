import requests
import json
import os
from dotenv import load_dotenv
from lodestoneScrape import get_character_image
from pprint import pprint

load_dotenv()

URL = os.getenv('FFLOGSAPI_URL')
TOKEN = os.getenv('BEARER_TOKEN')

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

with open('../resources/regions.json', 'r') as file:
    regions = json.load(file)
    pprint(regions)

def get_character(name:str, server:str):

    with open("../queries/character.graphql", "r") as file:
        query = file.read()
