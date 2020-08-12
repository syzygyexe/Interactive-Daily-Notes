import sqlite3
from models.db import db

# This model has two APIs, which are - find_by_username and find_by_id.
class UserModel(db.Model):
    # tell SQLAlchemy the table name, where these models are going to be stored:
    __tablename__ = "users"

    # primary_key=True == unique index
    # id is automatically generated 1,2,3,4,5, and we don't have to create _id arg,
    # as well as defining it inside of the __init__ as a self.id object
    id = db.Column(db.Integer, primary_key=True)
    # 80 characters maximum
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    # Above propertries mast match self.id/self.username/self.passowrd.
    # Otherwise, they won't be appended to the database.


    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            "id": self.id,
            "username": self.username
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        # since there is no same users, we are returning the very fist row .first()
        # SELECT * FROM users # second username is arg
        return cls.query.filter_by(username=username).first() 

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()