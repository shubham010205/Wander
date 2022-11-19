from datetime import date
from flask_login import UserMixin
from wander_flask import login_manager, db, marsh


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(20), nullable=False)
    blogs = db.relationship("Blog", backref="author", lazy=True)

    def __init__(self, first_name, last_name, username, email, password, image="default.jpg"):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.image = image


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=date.today)
    image = db.Column(db.String(20))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class UserSchema(marsh.Schema):
    class Meta:
        fields = ("username", "email")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class BlogSchema(marsh.Schema):
    class Meta:
        fields = ("title", "content", "date_posted")


post_schema = BlogSchema()
posts_schema = BlogSchema(many=True)