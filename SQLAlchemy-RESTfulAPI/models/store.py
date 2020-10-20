from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'             # Bug fix : user proper table name (must match with the created table name)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    items = db.relationship('ItemModel', lazy = 'dynamic')    # one to many so items are list type

    def __init__(self,name):
        self.name = name
        

    def json(self):
        return {'name' : self.name, 'items' : [item.json() for item in self.items.all()]} # because of lazy= dynamic we use .all() to get  all the items
    
    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name = name).first() # SELECT * FROM items WHERE name= name LIMIT 1
        

    def save_to_db(self):
        db.session.add(self)        # sql alchemy directly save object as row...
        db.session.commit()

    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

'''
here, lazy operation required for .. If we have lots of items and if we create more stores then for each item 
    application will generate the object seperately which will be costly operation. So, thats why we need to lazy the operation.   
'''