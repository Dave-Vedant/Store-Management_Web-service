from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',                    # beside of getting whole load, just load price field to change price only for same product.
            type =float,
            required = True,
            help = 'This field can not be left, plz use float type'
        )

    parser.add_argument('store_id',                    # beside of getting whole load, just load price field to change price only for same product.
            type =int,
            required = True,
            help = 'Every items need a store id '
        )

    @jwt_required()            # first authenticate then do the job, for each def need seperate use of jwt token (so, for delete , need to write same for auth)
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
           
    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message' : 'An item with name {} already exist.'.format(name)}, 400
        
        data = Item.parser.parse_args()

        item = ItemModel(name,**data) #  data['price'],data['store_id']) 
        try:
            item.save_to_db()
        except:
            return{'message' : 'An Error occured inserting thee items'}, 500 # internal server errors.
        
        return item.json(), 201

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message' : 'Item deleted'}
        

    def put(self,name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data) # data['price'],data['store_id']) 
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

    

class ItemList(Resource):           # Here, Resource is pregenerated class we just extendedly use it. 
    def get(self):
        return {'items' : [item.json() for item in ItemModel.query.all()]}  # SELECT * FROM items

        # or return {'item' : list(map(lambda x: x.json(), ItemModel.query.all() ))}