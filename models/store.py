from models.db import db

# db.Model allows us to save to database and retrieve from the database. (Mapping between db and objects)
class StoreModel(db.Model):
    __tablename__ = "stores"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # SQLAlchemy creates a relationship between ItemModel
    # this variable is the item list. Because it knows there can be a lot of items with the same store ID.
    # if we have a lot of items, we can tell SQLAlchemy do not go into the items table and create
    # an object for each item yet. (lazy="dynamic")
    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def json(self):
        # .all() is only used with lazy="dynamic". It makes self.items no longer a list of items
        # but a query builder that has the ability to look into the items table, then we can use .all()
        # to retrieve all items from that table. Which means that until we call the JSON method
        # we are not looking into the table. Which means that creating stores is very simple.
        # However, whenever we call the JSON method, we have to go into the table, it gonna be slower.
        # https://medium.com/@ns2586/sqlalchemys-relationship-and-lazy-parameter-4a553257d9ef
        return {
        "id": self.id,
        "name": self.name,
        "items": [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        # SELECT * FROM items WHERE name=name LIMIT 1. Basically improved return function 
        return cls.query.filter_by(name=name).first() 

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
