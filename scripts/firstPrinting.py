import json, os, requests


def get_first_printings():
    with open('../bulkData/scryfall-default-cards.json', 'r') as f:
        file_json = json.load(f)

    first_printings = []

    for card in file_json:
        if not card['reprint']:
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
    filename = '../images/' + str(name)
    filepath = os.path.join(dirname, filename)

    with open(filepath, 'wb') as f:
        f.write(r.content)

if __name__ == '__main__':
    card_list = get_first_printings()
    save_image_file(card_list[0]['image'], card_list[0]['name'])
