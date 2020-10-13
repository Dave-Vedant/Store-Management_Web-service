'''
Good Code Practice
'''
from flask import Flask, request 
from flask_restful import Resource, Api, reqparse  

from flask_jwt import JWT, jwt_required
from security import authenticate, identity

from user import User

app = Flask(__name__)
app.secret_key = 'orca'
api = Api(app)

jwt = JWT(app, authenticate, identity) 

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
        item = next(filter(lambda x:x['name'] == name, items), None)     # next will give one item at a time, and give all one by one with operate next.
        return {'item' : item}, 200 if item is not None else 404                       
    
    @jwt_required()
    def post(self,name): 
        if next(filter(lambda x: x['name']== name, items),None) is not None:
            return {'message' : 'An item with name {} already exist.'.format(name)}, 400
        
        data = Item.parser.parse_args()

        item = {'name' :name , 'price': data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self,name):
        global items           # say python that is item[] from global 
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message' : 'Item deleted'} 

    @jwt_required()
    def put(self,name):
        data = Item.parser.parse_args()
        
        item = next(filter(lambda x: x['name'] == name, items),None)
        if item is None:
            item = {'name' : name, 'price' : data['price']}
            items.append(item)
        else: 
            item.update(data)
        return item

class ItemList(Resource):           # Here, Resource is pregenerated class we just extendedly use it. 
    def get(self):
        return{'items': items}
    
api.add_resource(Item, '/item/<string:name>')    # local_url/studnt/name
api.add_resource(ItemList, '/items')             # item list

app.run(port=5000, debug=True)          