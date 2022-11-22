import os
from secrets import token_hex
from PIL import Image
from flask import current_app


def save_image(image):
    if not image:
        return None
    hashed = token_hex(8)
    _, file_ext = os.path.splitext(image.filename)
    image_name = hashed + file_ext
    image_path = os.path.join(current_app.root_path, "static/profile_pics", image_name)

    size = (525,525)
    i = Image.open(image)
    i.thumbnail(size=size)
    i.save(image_path)

    return image_name
