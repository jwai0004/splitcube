import requests

payload = { 'fuzzy' : 'Jace the mind',
            'format' : 'image',
            'version': 'png',
            }

named_url = 'https://api.scryfall.com/cards/named'

r = requests.get(named_url, payload)

with open('images/test.jpg', 'wb') as f:
    f.write(r.content)
