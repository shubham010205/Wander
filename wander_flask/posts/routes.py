from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user
from wander_flask import db
from wander_flask.models import Blog
from wander_flask.posts.utils import save_image
from wander_flask.posts.forms import CreatePostForm


posts = Blueprint("posts",__name__)

@posts.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        get_post = Blog(title=form.title.data, content=form.content.data, 
                            author=current_user, image=save_image(form.image.data))
        db.session.add(get_post)
        db.session.commit()
        flash("Blog has got added successfully!", "success")
        return redirect(url_for("main.home"))
    return render_template("create_post.html", form=form, title="Let's Post", legend="Let's Post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    get_post = Blog.query.get_or_404(post_id)
    if get_post.image:
        post_image = url_for('static', filename='/profile_pics/' + get_post.image)
    else:
        post_image = None
    return render_template("post.html", post=get_post, title=get_post.title, image=post_image)

@posts.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    get_post = Blog.query.get_or_404(post_id)
    db.session.delete(get_post)
    db.session.commit()
    flash("Blog Post has got deleted successfully!", "success")
    return redirect(url_for("main.home"))

@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    get_post = Blog.query.get_or_404(post_id)
    form = CreatePostForm()
    if form.validate_on_submit():
        get_post.title = form.title.data
        get_post.content = form.content.data
        get_post.image = save_image(form.image.data)
        db.session.commit()
        flash("Post has got updated successfully!", "success")
        return redirect(url_for("main.home"))
    elif request.method == "GET":
        form.title.data = get_post.title
        form.content.data = get_post.content
    return render_template("create_post.html", title = get_post.title,
                                form=form, legend="Post Update")
