import requests
import json
import os
from dotenv import load_dotenv
from fflogs.lodestoneScrape import get_character_image
from pprint import pprint

load_dotenv()

URL = os.getenv('FFLOGSAPI_URL')
TOKEN = os.getenv('BEARER_TOKEN')
RESOURCE_DIR = os.getenv('RESOURCE_DIR')

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

def process_server_info():
    #process regions json into set and dict
    with open('resources/regions.json', 'r') as file:
        regions = json.load(file)
        server_set = set()
        server_to_region = {}
        for region in regions:
            server_set.update(region['severSlugs'])
            server_to_region.update({server: region['serverRegion'] for server in region['severSlugs']})
    return server_set,server_to_region

def process_rankings(rankings:dict):
    #pprint(rankings)
    overall = {}
    parses = []
    overall['bestPerformanceAverage'] = rankings['bestPerformanceAverage']
    overall['medianPerformanceAverage'] = rankings['medianPerformanceAverage']
    with open("resources/zones.json", "r") as file:
        zones = json.load(file)
        #print(zones)
        for zone in zones:
            if zone['id'] == rankings['zone']:
                overall['zoneName'] = zone['name']
                break
    for parse in rankings['rankings']:
        parse_dict = {}
        parse_dict['bossName'] = parse['encounter']['name']
        parse_dict['id'] = parse['encounter']['id']
        parse_dict['rankPercent'] = parse['rankPercent']
        parse_dict['totalKills'] = parse['totalKills']
        parse_dict['bestSpec'] = parse['bestSpec']
        parse_dict['rank'] = parse['allStars']['rank']
        parses.append(parse_dict)
    return overall,parses
    #pprint(overall)
    #pprint(parses)


def get_character(name:str, server:str):
    server_set,server_dict = process_server_info()
    if server not in server_set:
        return None
    with open("queries/character.graphql", "r") as file:
        query = file.read()

        variables = {
            "name": name,
            "serverSlug": server,
            "serverRegion": server_dict[server]
        }
        response = requests.post(URL, headers=headers, json={'query': query, 'variables': variables})
        if response.status_code == 200:
            data = response.json()
            character = data['data']['characterData']['character']
            overall,parses = process_rankings(character['zoneRankings'])
        else:
            print(f"Failed to get character: {response.status_code}")
            return None
    #print(character['lodestoneID'])
    thumbnail = get_character_image(character['lodestoneID'])
    package = {
        'id': character['id'],
        'name': character['name'],
        'server': server,
        'thumbnail': thumbnail,
        'overall': overall,
        'parses': parses
    }
    pprint(package)
    return package
