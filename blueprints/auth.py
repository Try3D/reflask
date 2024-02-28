from flask import Blueprints, request, jsonify
from flask_bcrypt import bcrypt

from db import User, db

auth = Blueprints("views", __name__)


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return jsonify({"userid": user.userid})
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"userid": new_user.id})


@auth.route("/user", methods=["GET"])
def get_user():
    user_id = request.args.get("userid")
    user = User.query.filter_by(id=user_id).first()

    if user:
        return jsonify({"userid": user.id, "email": user.email})
    else:
        return jsonify({"error": "User not found"}), 404
