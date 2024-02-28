from flask import Flask
from flask_cors import CORS
from db import db

from blueprints.auth import auth

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SECRET_KEY"] = "SECRET_KEY"

db.init_app(app)

CORS(app)

# Register your blueprints here
app.register_blueprint(auth, url_prefix="/auth")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
