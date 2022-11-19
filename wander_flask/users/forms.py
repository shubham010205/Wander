from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_login import current_user
from wander_flask.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(),Length(min=2,max=20)])
    last_name = StringField("Last Name", validators=[DataRequired(),Length(min=2,max=20)])
    username = StringField("Username", validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", 
                                        validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("The username already exist! Try a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("The email already exist! Use a different email id.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class AccountUpdateForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(),Length(min=2,max=20)])
    last_name = StringField("Last Name", validators=[DataRequired(),Length(min=2,max=20)])
    username = StringField("Username", validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField("Email", validators=[DataRequired(),Email()])
    image = FileField("Profile Picture", validators=[FileAllowed(["jpg","png"])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("The username already exist! Try a different one.")

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("The email already exist! Use a different email id.")


class ResetPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()])
    submit = SubmitField("Send Reset Mail")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("The email doesn't exist! Please check your email address.")