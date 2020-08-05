from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
# encryption
app.secret_key = "jose"
# add api
api = Api(app)
