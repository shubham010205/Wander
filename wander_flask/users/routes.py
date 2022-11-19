from secrets import token_hex
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user
from wander_flask import db, bcrypt
from wander_flask.models import User, Blog
from wander_flask.main.utils import save_image, send_password_reset_mail
from wander_flask.users.forms import (RegistrationForm, LoginForm,
                                        AccountUpdateForm, ResetPasswordForm)


users = Blueprint("users",__name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("You have registered successfully! You can sign in now.", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form, title="Register")

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Welcome aboard!", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful! Please check your credentials.", "danger")
    return render_template("login.html", form=form, title="Login")

@users.route("/account")
@login_required
def account():
    image = url_for('static', filename='/profile_pics/'+current_user.image)
    return render_template("account.html", image=image, title="Account")

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account/update", methods=["GET", "POST"])
@login_required
def update():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.image.data:
            current_user.image = save_image(form.image.data)
        db.session.commit()
        flash("Account info updated successfully!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account_update.html", form=form, title="Update Account")

@users.route("/profile/<int:user_id>")
def profile(user_id):
    user = User.query.get_or_404(user_id)
    image = url_for('static', filename='/profile_pics/'+user.image)
    posts = Blog.query.filter_by(author_id=user_id).all()
    return render_template("profile.html", title=user.username, posts=posts, image=image, user=user)

@users.route("/reset_password", methods=["GET","POST"])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        token = token_hex(16)
        reset_mail = send_password_reset_mail(email=form.email.data,token=token)
        if reset_mail:
            flash("Password Reset mail sent successfully!", "info")
            return redirect(url_for("users.login"))
    return render_template("reset_password.html", form=form, title="Reset Password")
