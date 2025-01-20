import os
import requests
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

URL = os.getenv('FFLOGSAPI_URL')
TOKEN = os.getenv('BEARER_TOKEN')

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

def get_zones():
    with open("queries/zones.graphql", "r") as file:
        query = file.read()
    response = requests.post(URL, headers=headers, json={'query': query})
    if response.status_code == 200:
        data = response.json()
        zones = data['data']['worldData']
        with open("resources/zones.json", "w") as file:
            file.write(str(zones))
    else:
        print(f"Failed to get zones: {response.status_code}")

def get_jobs():
    with open("queries/jobs.graphql", "r") as file:
        query = file.read()
    response = requests.post(URL, headers=headers, json={'query': query})
    if response.status_code == 200:
        data = response.json()
        jobs = data['data']['gameData']['classes'][0]['specs']
        # Note: The jobs are a list of dictionaries.
        with open("resources/jobs.json", "w") as file:
            file.write(str(jobs))
    else:
        print(f"Failed to get jobs: {response.status_code}")

def get_regions():
    # regions slug = serverRegion
    # subregion name = serverSlug
    with open("queries/regions.graphql", "r") as file:
        query = file.read()
    response = requests.post(URL, headers=headers, json={'query': query})
    if response.status_code == 200:
        data = response.json()
        regions = data['data']['worldData']
        with open("resources/regions.json", "w") as file:
            file.write(str(regions))
    else:
        print(f"Failed to get regions: {response.status_code}")
