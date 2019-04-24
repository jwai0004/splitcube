import json, os, requests, time, csv
from pathvalidate import sanitize_filename
import combineImages, getFirstPrintings, paths

def save_image_file(card):
    '''
    Takes a card object, requests its image and saves to file
    returns filepath
    '''
    name = card['name']
    image_url = card['image']

    filepath = paths.imageName(name, subfolder='cards/')

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
    '''
    Takes the path to a csv file and generates images for all cards in the file
    returns a list of all split card_names
    '''
    # TODO Refactor this, it seems to do a lot and have lots of side effects and a weird
    # return value

    card_dict = getFirstPrintings.get_first_printings()
    cards_to_find = get_cards_from_file(csv)
    card_name_list = []

    for cards in cards_to_find:
        card_name = cards[0] + '-' + cards[1]
        card_name_list.append(sanitize_filename(card_name))
        filename = paths.imageName(card_name, subfolder='splitcards/')

        if not os.path.isfile(filename):
            img1 = save_image_file(card_dict[cards[0]])
            img2 = save_image_file(card_dict[cards[1]])

            print(f'Combining {filename}')
            combineImages.combine_cards(img1, img2, filename)

    return card_name_list


def generate_PDF(card_list):

    path_list = [ paths.imageName(c, subfolder='splitcards') for c in card_list ]

    # Break list into sublists of length 9
    page_chunks = [ path_list[x:x+9] for x in range(0, len(path_list), 9) ]

    pages = [
            combineImages.create_page(chunk, f'page{i}')
            for i, chunk in enumerate(page_chunks)
            ]

    combineImages.images_to_pdf(pages)
    print(f'{len(pages)} pages were generated')

if __name__ == '__main__':
    csv_path = paths.projectPath(suffix='smallCardList.csv')
    card_list = create_splitcards_from_file(csv_path)
    generate_PDF(card_list)
