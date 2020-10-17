'''
Good Code Practice
'''
from flask import Flask
from flask_restful import Api

from flask_jwt import JWT, jwt_required
from security import authenticate, identity

from user import User
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'orca'
api = Api(app)

jwt = JWT(app, authenticate, identity) 

# Going to use seperate item file 

api.add_resource(Item, '/item/<string:name>')    # local_url/studnt/name
api.add_resource(ItemList, '/items')             # item list
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(port = 5000, debug = True)

