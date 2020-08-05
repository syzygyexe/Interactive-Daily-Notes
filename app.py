from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
# encryption
app.secret_key = "jose"
# add api
api = Api(app)

# JWT creates a new endpoint - /auth. When we call a /auth, we send it a username and a password,
# and the JWT extension gets that username and password and sends it over to the authenticate function
# that takes in a username and password. We are then going to find the correct user object,
# using that username, and we are going to compare its password to the one we received through
# the /auth endpoint.
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items/")
# When we are going to call "/register" with "POST method", we will execute UserRegister method.
api.add_resource(UserRegister, "/register/")


if __name__ == "__main__":
    app.run(port=5000, debug=False)
