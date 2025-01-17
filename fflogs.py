import os
from dotenv import load_dotenv
from fflogsapi import FFLogsClient
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
client = FFLogsClient(CLIENT_ID,CLIENT_SECRET)
character = client.get_character(filters={'name':'Popi Pipapo','serverSlug':'Sephirot','serverRegion':'OC'})

print(character.name())


client.close()
