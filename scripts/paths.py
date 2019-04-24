import os
from pathvalidate import sanitize_filename

def projectPath(suffix=''):
    currentFilePath = os.path.dirname(__file__)
    parent = os.path.join(currentFilePath, '../')

    if suffix:
        parent = os.path.join(parent, suffix)

    return parent

def imageName(card_name, subfolder=''):
    dirname = projectPath(suffix='images/')
    filename = sanitize_filename(card_name) + '.png'

    if subfolder:
        filename = os.path.join(subfolder, filename)

    imagePath = os.path.join(dirname, filename)

    return imagePath
