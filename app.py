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

# JWT creates a new endpoint /login/
app.config["JWT_AUTH_URL_RULE"] = "/login/"
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items/")
# When we are going to call "/register" with "POST method", we will execute UserRegister method.
api.add_resource(UserRegister, "/register/")


if __name__ == "__main__":
    app.run(port=5000, debug=False)
