from PIL import Image
from fpdf import FPDF
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

    combined = combined.rotate(90, expand=1)
    combined.save(target)

    return combined

def create_page(image_list, name):
    '''
    Takes a list of 9 card images and combines into a grid image
    '''

    img = Image.open(image_list[0])
    CARD_WIDTH, CARD_HEIGHT = img.size

    grid = Image.new('RGBA', (3*CARD_WIDTH, 3*CARD_HEIGHT))

    for j in range(3):
        for i in range(3):
            img = Image.open(image_list[j*3 + i])
            grid.paste(img, (i*CARD_WIDTH, j*CARD_HEIGHT))


    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../images/pages/' + name + '.png')
    grid.save(filename)

    return filename

def images_to_pdf(images):
    '''
    Takes a list of images and creates a pdf with one per page
    '''
    pdf = FPDF()
    for image in images:
        pdf.add_page()
        pdf.image(image, 10, 15, 189, 264)
    pdf.output('SplitCube.pdf', 'F')


if __name__ == '__main__':

    card_list = [
            "Siege Rhino-Verdant Catacombs",
            "Jace, the Mind Sculptor-Ancestral Recall",
            "Turn  Burn-Niv-Mizzet, Parun",
            "Garruk Wildspeaker-Birthing Pod",
            "History of Benalia-Balance",
            "Aether Adept-True-Name Nemesis",
            "Volcanic Island-Steam Vents",
            "Library of Alexandria-Sword of Feast and Famine",
            "Tarmogoyf-Life from the Loam",
            ]

    path_list = [ '../images/splitcards/' + c + '.png' for c in card_list ]
    dirname = os.path.dirname(__file__)

    path_list = [ os.path.join(dirname, path) for path in path_list ]

    page = create_page(path_list, '1')
    images_to_pdf([page, page])
