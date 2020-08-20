from models.db import db

# db.Model allows us to save to database and retrieve from the database. (Mapping between db and objects)
class ItemModel(db.Model):
    __tablename__ = "items"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # precision=2, stands for the number of numbers after the decimal point.
    price = db.Column(db.Float(precision=2))
    # stores is the table name of the store  .id - column
    # foreign key reference is sort of "subsidiary" key, which has limited credentials.
    # basically now we give ID additional parameter, what store do we belong to?
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    # Creates relationship between store id and every item in our database.
    store = db.relationship("StoreModel")

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
        "id": self.id,
        "name": self.name,
        "price": self.price,
        "store_id": self.store_id
        }

    @classmethod
    def find_by_name(cls, name):
        # query is not something we have defined, it something that comes from db.Model
        # We have class. Then we say we want to query the model. And then we say filter by.
        # In other words SELECT * FROM items WHERE name=name(second name is our arg inside of find_by_name method)
        # Translates this code onto SQLCode, this data is also being converted to an item model object.
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1, basically returns only 

    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self):
        # it is saving the model to the data base, SQLAlchemy can directly transform object to a row.
        # we are adding the collection of objects
        # this method is useful for both update and insert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
