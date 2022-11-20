from flask import Blueprint, render_template
from wander_flask.models import Blog


main = Blueprint("main",__name__)

@main.route("/")
@main.route("/home")
def home():
    posts = Blog.query.all()
    return render_template("home.html", posts=posts)

@main.route("/about")
def about():
    return render_template("about.html", title="About")
