import json, os, requests, time, csv
from pathvalidate import sanitize_filename

def save_image_file(card):
    '''
    Takes a card object, requests its image and saves to file
    returns filepath
    '''
    name = card['name']
    image_url = card['image']

    dirname = os.path.dirname(__file__)
    filename = '../images/' + sanitize_filename(name) + '.png'
    filepath = os.path.join(dirname, filename)

    if not os.path.isfile(filepath):
        print(f'Downloading {name}')
        r = requests.get(image_url)
        # Sleep to avoid overloading api
        time.sleep(0.075)

        with open(filepath, 'wb') as f:
            f.write(r.content)
    return filepath


def get_cards_from_file(filename):
    '''
    Reads pairs of cards from file and returns them as list of pairs
    '''
    card_list = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                card_list.append((row[0], row[1]))
    return card_list


def create_splitcards_from_file(csv):
    from combineImages import combine_cards
    from getFirstPrintings import get_first_printings

    card_dict = get_first_printings()
    cards_to_find = get_cards_from_file(csv)

    for cards in cards_to_find:
        filename = '../images/splitcards/' + \
                sanitize_filename(cards[0]) + \
                '-' + \
                sanitize_filename(cards[1]) + \
                '.png'

        if not os.path.isfile(filename):
            img1 = save_image_file(card_dict[cards[0]])
            img2 = save_image_file(card_dict[cards[1]])

            dirname = os.path.dirname(__file__)

            target = os.path.join(dirname, filename)

            print(f'Combining {target}')
            combine_cards(img1, img2, target)

if __name__ == '__main__':
    create_splitcards_from_file('smallCardList.csv')
