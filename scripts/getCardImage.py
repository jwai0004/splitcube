import json, os, requests, time, csv
from pathvalidate import sanitize_filename

def get_first_printings():
    '''
    Reads a JSON file from scryfall and creats a list of card objects
    with only the first printing of each card
    '''
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../bulkData/scryfall-default-cards.json')


    # Would likely be faster and much more memory efficient to process
    # one card at a time by reading single lines
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


def card_list_to_dict(card_list):
    '''
    Takes list of card objects and returns them as a dict with card names as keys
    '''
    card_dict = dict()
    for card in card_list:
        name = card['name']
        card_dict[name] = card

    return card_dict


def save_image_file(card):
    '''
    Takes a card object, requests its image and saves to file
    '''
    name = card['name']
    image_url = card['image']

    dirname = os.path.dirname(__file__)
    filename = '../images/' + sanitize_filename(name) + '.jpg'
    filepath = os.path.join(dirname, filename)

    if not os.path.isfile(filepath):
        r = requests.get(image_url)
        time.sleep(0.05)

        with open(filepath, 'wb') as f:
            f.write(r.content)


def get_cards_from_file(filename):
    '''
    Gets a card name card
    '''
    card_list = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                card_list.append(row[0])
    return card_list


if __name__ == '__main__':
    card_list = get_first_printings()
    card_dict = card_list_to_dict(card_list)
    cards_to_find = get_cards_from_file('smallCardList.csv')

    for card in cards_to_find:
        save_image_file(card_dict[card])
