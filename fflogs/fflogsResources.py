import json
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
    with open("../queries/zones.graphql", "r") as file:
        query = file.read()
    response = requests.post(URL, headers=headers, json={'query': query})
    if response.status_code == 200:
        data = response.json()
        zones = data['data']['worldData']['zones']
        with open("../resources/zones.json", "w") as file:
            json.dump(zones, file, indent=4)
    else:
        print(f"Failed to get zones: {response.status_code}")

def get_jobs():
    with open("../queries/jobs.graphql", "r") as file:
        query = file.read()
    response = requests.post(URL, headers=headers, json={'query': query})
    if response.status_code == 200:
        data = response.json()
        jobs = data['data']['gameData']['classes'][0]['specs']
        # Note: The jobs are a list of dictionaries.
        with open("../resources/jobs.json", "w") as file:
            json.dump(jobs, file, indent=4)
    else:
        print(f"Failed to get jobs: {response.status_code}")

def get_regions():
    with open("../queries/regions.graphql", "r") as file:
        query = file.read()
    response = requests.post(URL, headers=headers, json={'query': query})
    if response.status_code == 200:
        data = response.json()
        regions = data['data']['worldData']['regions']
        new_regions = []
        slugs_only = []
        for region in regions:
            if region['slug'] in ['CN','KR']:
                continue
            tmp = {}
            tmp['serverRegion'] = region['slug']
            tmp['severSlugs'] = []
            for server in region['servers']['data']:
                tmp['severSlugs'].append(server['name'])
                slugs_only.append(server['name'])
            new_regions.append(tmp)
        with open("../resources/regions.json", "w") as file:
            json.dump(new_regions, file, indent=4)
        with open("../resources/serverSlugs.json", "w") as file:
            json.dump(slugs_only, file, indent=4)
    else:
        print(f"Failed to get regions: {response.status_code}")


def main():
    get_zones()
    get_jobs()
    get_regions()


if __name__ == "__main__":
    main()