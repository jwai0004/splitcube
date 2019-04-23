import json, os, pickle

PKL_FILE = 'firstPrinting.pkl'

def get_first_printings():
    '''
    Reads a JSON file from scryfall and creats a dict of card objects
    with only the first printing of each card with card names as keys
    '''

    # If already processed just use cache
    if os.path.isfile(PKL_FILE):
        return read_cards_from_file(PKL_FILE)

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../bulkData/scryfall-default-cards.json')


    # Would likely be faster and much more memory efficient to process
    # one card at a time by reading single lines
    with open(filename, 'r') as f:
        file_json = json.load(f)

    first_printings = dict()

    for card in file_json:
        # Process only if first printing from main set
        if not card['reprint'] and len(card['set']) == 3:
            try:
                card_dict = {
                    'name': card['name'],
                    'set': card['set'],
                    'image': card['image_uris']['png']
                    }
                first_printings[card_dict['name']] = card_dict
            except KeyError:
                # Only KeyErrors dectected are from double faced cards
                # This could change and break things
                card_dict = {
                    'name': card['card_faces'][0]['name'],
                    'set': card['set'],
                    'image': card['card_faces'][0]['image_uris']['png']
                    }

                first_printings[card_dict['name']] = card_dict

                card_dict = {
                    'name': card['card_faces'][1]['name'],
                    'set': card['set'],
                    'image': card['card_faces'][1]['image_uris']['png']
                    }

                first_printings[card_dict['name']] = card_dict

    write_cards_to_file(first_printings)

    return first_printings


def write_cards_to_file(card_dict):
    with open(PKL_FILE, 'wb') as f:
        pickle.dump(card_dict, f, pickle.HIGHEST_PROTOCOL)


def read_cards_from_file(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    get_first_printings()
