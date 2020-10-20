from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
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
        item = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404
           
    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message' : 'An Store with name {} already exist.'.format(name)}, 400
        
        store = StoreModel(name) 

        try:
            store.save_to_db()
        except:
            return{'message' : 'An Error occured inserting the store'}, 500 # internal server errors.
        
        return store.json(), 201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        
        return {'message' : 'Store deleted'}

    

class StoreList(Resource):           # Here, Resource is pregenerated class we just extendedly use it. 
    def get(self):
        return {'stores' : [store.json() for store in StoreModel.query.all()]}  # SELECT * FROM items

        # or return {'stores' : list(map(lambda x: x.json(), StoerModel.query.all() ))}