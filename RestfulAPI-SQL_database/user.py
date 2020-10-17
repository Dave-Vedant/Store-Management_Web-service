import sqlite3
from flask_restful import Resource, reqparse

class User():   
    def __init__(self, _id, username, password):    
        self.id = _id
        self.username = username
        self.password = password

    @classmethod 
    def find_by_username(cls,username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)   # (*row) = (row[0],row[1],row[2])
        else:
            user = None

        connection.close()
        return user

    @classmethod 
    def find_by_id(cls,_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE id=?"  # Bug fixed "was username --> changed to id , WOW! "
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)   # (*row) = (row[0],row[1],row[2])
        else:
            user = None
        
        connection.close()
        return user

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type= str,
        required = True,
        help = "This field can not be blank.")

    parser.add_argument('password',
        type = str,
        required = True,
        help = "This field can not be blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):        # username duplication fix
            return{'message': 'A user with the username is already exist, choose other username'}, 400
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(query, (data['username'],data['password']))
        
        connection.commit()      # to save to disk...
        connection.close()

        return {'message' : '{} named User created successfully.'.format(data['username'])}, 201        
        