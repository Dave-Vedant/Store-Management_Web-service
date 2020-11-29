from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.user import UserRegister, User, UserLogin, Token_Refresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'dave117' # app.config['JWT_SECREAT_KEY'] # these values use to encrept jwt token
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)  # due to jwt manager auth endpiont will not genereate so we need to make it from ourside.

# introduce jwt claim for admin role (to delete)
@jwt.user_claims_loader
def claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

# 
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'Hey! Are you there?, The Token has expired.',
        'error': 'token_expired'
    }), 401

# when token does not match value
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'What are you Doing?',
        'error': 'wrong token value!'
    }), 401

# unauthorized
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description' : 'Request does not contain an access token.',
        'error': 'authorization required'
    }), 401

# when token is not fresh
@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh token required'
    }), 401

# token is revoked 
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description' : 'The Token has been revoked.',
        'error' : 'token revoked'
    }), 401


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(Token_Refresh,'/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

