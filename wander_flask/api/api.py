from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, create_access_token
from wander_flask import db, bcrypt
from wander_flask.models import (User, user_schema, users_schema,
                                    Blog, posts_schema)


api = Blueprint("api", __name__)

class Users(MethodView):
    def get(self):
        email = request.form.get("email")
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                data = user_schema.dump(user)
                return jsonify(user= data)
            else:
                return jsonify(message= "The email does not belongs to a user's account!"), 404
        else:
            users = User.query.all()
            data = users_schema.dump(users)
            return jsonify(users= data)

    def post(self):
        email = request.form.get("email")
        username = request.form.get("username")
        if username or email:
            user1 = User.query.filter_by(email=email).first()
            user2 = User.query.filter_by(username=username).first()
            if user1 or user2:
                return jsonify(message= "These user details already exist."), 401
            else:
                hashed_password = bcrypt.generate_password_hash(request.form.get("password")).decode("utf-8")
                user = User(first_name= request.form.get("first_name"),
                                last_name= request.form.get("last_name"),
                                username= username,
                                email= email,
                                password= hashed_password
                                )
                db.session.add(user)
                db.session.commit()
                return jsonify(message= "User has got created successfully")
        else:
            return jsonify(message= "Please enter the details to create a user.",
                            keys= "first_name, last_name, username, email, password"), 400

    # @jwt_required
    def put(self):
        email = request.form.get("email")
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                user.first_name = request.form.get("first_name"),
                user.last_name= request.form.get("last_name"),
                user.username= request.form.get("username"),
                user.email= email,
                user.password= request.form.get("password")
                
                db.session.commit()

                return jsonify(message= "User details have got updated successfully!")
            else:
                return jsonify(message= "The email does not belongs to a user's account!"), 404

        else:
            return jsonify(message= "Please enter the details to update a user.",
                            keys= "first_name, last_name, username, email, password"), 400


    # @jwt_required
    def delete(self):
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(message= "User has got deleted successfully!")
        else:
            return jsonify(message= "The email does not belongs to a user's account!"), 400


view_function = Users.as_view("users_api")
api.add_url_rule("/api/users", methods= ["GET", "POST"],
                            view_func= view_function)


@api.route("/api/users/login", methods=["POST"])
def login_api_user():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email= email, password=password).first()
    if user:
        token = create_access_token(identity=email)
        return jsonify(token= token, message= "Login Successful! Auth Token created!")
    else:
        return jsonify(message= "Please check your login credentials!")


class Posts(MethodView):
    def get(self):
        author_id = request.form.get("author_id")
        if author_id:
            posts = Blog.query.filter_by(author_id=int(author_id)).all()
            if posts:
                data = posts_schema.dump(posts)
                return jsonify(data= data)
            else:
                return jsonify(message= "The user hasn't posted anything yet!")
        else:
            posts = Blog.query.all()
            data = posts_schema.dump(posts)
            return jsonify(data= data)

view_funcs = Posts.as_view("posts_api")
api.add_url_rule("/api/posts", methods= ["GET"], view_func= view_funcs)
