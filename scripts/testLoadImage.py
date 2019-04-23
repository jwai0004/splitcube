import requests
import os

payload = { 'fuzzy' : 'Jace the mind',
            'format' : 'image',
            'version': 'png',
            }

named_url = 'https://api.scryfall.com/cards/named'

r = requests.get(named_url, payload)

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../images/test.jpg')

with open(filename, 'wb') as f:
    f.write(r.content)
