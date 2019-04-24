from PIL import Image
from fpdf import FPDF
import paths


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

    # Dramatic performance improvement by changing this from RGBA to RGB
    grid = Image.new('RGB', (3*CARD_WIDTH, 3*CARD_HEIGHT))

    for j in range(3):
        for i in range(3):
            try:
                img = Image.open(image_list[j*3 + i])
            except:
                img = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), color='#FFFFFF')

            grid.paste(img, (i*CARD_WIDTH, j*CARD_HEIGHT))

    filename = paths.imageName(name, subfolder='pages')
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

    filename = paths.projectPath(suffix='SplitCube.pdf')
    pdf.output(filename, 'F')
