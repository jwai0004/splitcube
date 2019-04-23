from PIL import Image
import os

def combine_cards(card1, card2, target):
    '''
    Given the path to two cards, combine them into a single image
    '''
    img1 = Image.open(card1)
    img2 = Image.open(card2)

    CARD_WIDTH, CARD_HEIGHT = img1.size

    # TODO improve the colour matching and maybe trim borders
    combined = Image.new('RGBA', (2*CARD_WIDTH, CARD_HEIGHT), color='#111111')

    combined.paste(img1, (0, 0), mask=img1)
    combined.paste(img2, (CARD_WIDTH, 0), mask=img2)

    combined.save(target)

if __name__ == '__main__':

    dirname = os.path.dirname(__file__)
    path1 = '../images/Jace, the Mind Sculptor.png'
    path2 = '../images/Library of Alexandria.png'
    targetpath = '../images/splitcards/Jace Pod.png'
    filepath1 = os.path.join(dirname, path1)
    filepath2 = os.path.join(dirname, path2)
    target = os.path.join(dirname, targetpath)

    combine_cards(filepath1, filepath2, target)
