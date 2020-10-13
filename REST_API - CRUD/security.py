from werkzeug.security import safe_str_cmp
from user import User  

users = [
    User(1,'bob','bob123')      # (id, user_nane, password), kind of database...
]

username_mapping = { u.username: u for u in users}
userid_mapping = {u.id : u for u in users}            # see reference at bottom...


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)

'''
# Easy because of importing user.py 
userid_mapping = { 1: {
    'id' : 1,
    'username' : 'bob',
    'password' : 'bob123'
}}
'''