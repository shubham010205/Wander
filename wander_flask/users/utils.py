import os
from secrets import token_hex
from PIL import Image
from flask import current_app
from flask_mail import Message
from wander_flask import mail


def save_image(image):
    if not image:
        return None
    hashed = token_hex(8)
    _, file_ext = os.path.splitext(image.filename)
    image_name = hashed + file_ext
    image_path = os.path.join(current_app.root_path, "static/profile_pics", image_name)

    size = (125,125)
    i = Image.open(image)
    i.thumbnail(size=size)
    i.save(image_path)

    return image_name

def send_password_reset_mail(email,token):
    msg = Message("WanderBlog Password Reset",
                    sender="admin@WanderBlog.com",
                    recipients=[email])
    msg.body = (f"Hello {email}. To reset your password please follow the link:\n"
                    f"https://localhost:5000/update_password?token={token}")
    mail.send(msg)
    return True
