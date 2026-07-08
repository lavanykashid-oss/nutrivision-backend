from PIL import Image
import imagehash


def generate_phash(image):

    image.seek(0)

    img = Image.open(image)

    phash = imagehash.phash(img)

    image.seek(0)

    return str(phash)