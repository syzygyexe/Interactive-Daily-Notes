from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
        create_access_token,
        create_refresh_token, 
        jwt_refresh_token_required,
        get_jwt_identity,
        jwt_required,
        get_raw_jwt
        )

from models.user import UserModel
from blacklist import BLACKLIST

# Create request parser that accepts username and password.
# This parser will parse through the JSON of the request and make sure username and password are there.
# underscore "_" at the start does not allow variable to be imported anywhere else(private variable).
_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
        "username",
        type=str,
        required=True,
        help="This field cann ot be blank.",
        )

_user_parser.add_argument(
        "password",
        type=str,
        required=True,
        help="This field cannot be blank.",
        )

class UserRegister(Resource):
    # create and save user to db.
    def post(self):
        # Fetching parsed data from the JSON payload. This expects to have username and password.
        data = _user_parser.parse_args()
        # check whether the usernmae exists or not. 
        # With data which is being passed through JSON we are checking with the help of find_by_username method of the User class.
        # MUST BE IN FRONT OF CONNECTION(!!!) in order not to cau se any bugs with open connection
        if UserModel.find_by_username(data["username"]) is not None:
            return {"message": "A user with that username already exists"}, 400
        # connect to database
        user = UserModel(**data) #data["username"], data["password"]
        user.save_to_db()
        # 201 - created
        return {"message": "User created succesfully."}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted."}, 200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()

        # find user in database
        user = UserModel.find_by_username(data["username"])

        # check password
        if user and safe_str_cmp(user.password, data["password"]):
            # look later
            # create an access token
            # create refresh token (we will look at this later!)
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200

        return {"message": "Invalid credentials"}, 401        

class UserLogout(Resource):
    @jwt_required
    def post(self):
         # blacklist current token, and force user to get a new token by logining-in
         # every token has a unique ID == jti
        jti = get_raw_jwt()['jti'] # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {"message": "Succesfully logged out."}, 200

class TokenRefresh(Resource):
    # will only run with refresh token
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        # fresh=True, means that all tokens would be fresh.
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
