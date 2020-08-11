from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, ItemList
# app >>> store(resources) >>> store(model) >>> table with definitions.
# If we are not going to track tables, the table for stores won't be created.
from resources.store import Store, StoreList

app = Flask(__name__)
# the database doesnt necessarily needs to be sqlite, it can be MySql/Oracle, anything.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# Turns off Flask_SQLAlchemy tracker, and sets SQLAlchemy modification tracker on.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Flask JWT will show you wrong messages in details, if one occurs.
app.config["PROPAGATE_EXCEPTIONS"] = True
# encryption
app.secret_key = "jose" # app.config["JWT_SECRET_KEY"]
# add api
api = Api(app)

# this method is going to be run before any method
@app.before_first_request
def create_tables():
    # this is going to create all tables inside of the db, unless they exist already
    db.create_all()

jwt = JWTManager(app) # not creating /auth, we have to create is ourselves inside of the user resources.

# inside of jwt variable!!!
@jwt.user_claims_loader
# parameter must be called "identity". In our case "identity" == "user.id"
def add_claims_to_jwt(identity):
    if identity == 1: # Instead of hard-coding, you should read from adcoding file or a database.
        return {"is_admin": True}
    return {"is_admin": False}

# inside of jwt variable!!!
@jwt.expired_token_loader
def expired_token_callback():
    


# token expiration time
# # config JWT to expire within half an hour
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)


#Authentication Key Name
# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(StoreList, "/stores/")
api.add_resource(ItemList, "/items/")
# When we are going to call "/register" with "POST method", we will execute UserRegister method.
api.add_resource(UserRegister, "/register/")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login/")
api.add_resource(TokenRefresh, "/refresh/")

if __name__ == "__main__":
    from models.db import db
    db.init_app(app)
    app.run(port=5000, debug=False)
