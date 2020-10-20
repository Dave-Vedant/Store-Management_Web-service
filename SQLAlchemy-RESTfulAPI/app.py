'''
Good Code Practice
'''
from flask import Flask
from flask_restful import Api

from flask_jwt import JWT, jwt_required
from security import authenticate, identity

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # say where to find the data.db DATAbase
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False # this turn off flask sql alchemy tracker but still sql_alchemy tracker is still in use (running)...
app.secret_key = 'bob'
api = Api(app)

@app.before_first_request         # No need of running create_table.py file now!, create data.db from above sqlite configurations.
def create_table():
    db.create_all()

jwt = JWT(app, authenticate, identity) 

# Going to use seperate item file 

api.add_resource(Item, '/item/<string:name>')    # local_url/studnt/name
api.add_resource(ItemList, '/items')          # item list
api.add_resource(Store, '/store/<string:name>')       # Bug fix : no space between string:name other wise url will be malfunctioning.
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db  
    db.init_app(app)
    app.run(port = 5000, debug = True)

