import hashlib


def generate_image_hash(image):

    image.seek(0)

    image_bytes = image.read()

    image.seek(0)

    return hashlib.sha256(image_bytes).hexdigest()