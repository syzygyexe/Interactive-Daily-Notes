from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
# Turns off Flask_SQLAlchemy tracker, and sets SQLAlchemy modification tracker on.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# encryption
app.secret_key = "jose"
# add api
api = Api(app)

# app.config["JWT_AUTH_URL_RULE"] = "/login"
jwt = JWT(app, authenticate, identity)

# token expiration time
# # config JWT to expire within half an hour
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)


#Authentication Key Name
# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items/")
# When we are going to call "/register" with "POST method", we will execute UserRegister method.
api.add_resource(UserRegister, "/register/")


if __name__ == "__main__":
    from models.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
