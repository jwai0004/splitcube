import json, os, requests
from pathvalidate import sanitize_filename

def get_first_printings():

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../bulkData/scryfall-default-cards.json')

    with open(filename, 'r') as f:
        file_json = json.load(f)

    first_printings = []

    for card in file_json:
        # Process only if first printing from main set
        if not card['reprint'] and len(card['set']) == 3:
            try:
                card_dict = {
                    'name': card['name'],
                    'set': card['set'],
                    'image': card['image_uris']['large']
                    }
                first_printings.append(card_dict)
            except KeyError:
                # Only KeyErrors dectected are from double faced cards
                # This could change and break things
                card_dict = {
                    'name': card['card_faces'][0]['name'],
                    'set': card['set'],
                    'image': card['card_faces'][0]['image_uris']['large']
                    }
                first_printings.append(card_dict)

                card_dict = {
                    'name': card['card_faces'][1]['name'],
                    'set': card['set'],
                    'image': card['card_faces'][1]['image_uris']['large']
                    }
                first_printings.append(card_dict)
    return first_printings


def save_image_file(image_url, name):
    r = requests.get(image_url)

    dirname = os.path.dirname(__file__)
    filename = '../images/' + sanitize_filename(name) + '.jpg'
    filepath = os.path.join(dirname, filename)

    with open(filepath, 'wb') as f:
        f.write(r.content)

if __name__ == '__main__':
    import random, time
    card_list = get_first_printings()
    for _ in range(10):
        ind = random.randint(0, len(card_list))
        print(card_list[ind]['name'])
        save_image_file(card_list[ind]['image'], card_list[ind]['name'])
        # Sleep for 100ms for around 10 requests per second
        time.sleep(0.1)
