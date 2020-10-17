import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

items = [] 

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',                    # beside of getting whole load, just load price field to change price only for same product.
            type =float,
            required = True,
            help = 'This field can not be left, plz use float type'
        )

    @jwt_required()            # first authenticate then do the job, for each def need seperate use of jwt token (so, for delete , need to write same for auth)
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404 
    

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?" 
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row is not None:
            return{'item' : {'name': row[0], 'price':row[1]}}
           
    def post(self,name):
        if Item.find_by_name(name):
            return {'message' : 'An item with name {} already exist.'.format(name)}, 400
        
        data = Item.parser.parse_args()

        item = {'name' :name , 'price': data['price']}

        try:
            Item.insert(item)
        except:
            return{'message' : 'An Error occured inserting thee items'}, 500 # internal server errors.
        
        return item, 201

    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?" 
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        return {'message' : 'Item deleted'} 

    def put(self,name):
        data = Item.parser.parse_args()
        
        item = Item.find_by_name(name)
        updated_item = {'name' : name, 'price' : data['price']}
        
        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return{ 'message' : 'An error occurred during inserting the item'}, 500
        else:
            try:
                Item.update(updated_item)
            except:
                return{'message' : 'An error occurred during updating the item'}
        return updated_item

    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (item['price'], item['name']))  # change sequence according to query...

        connection.commit()
        connection.close()

class ItemList(Resource):           # Here, Resource is pregenerated class we just extendedly use it. 
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)  # change sequence according to query...
        items = []
        for row in result:
            items.append({'name' : row[0], 'price' : row[1]})

        connection.close()

        return{'items': items}