from flask import request, jsonify
from src.service.instance import server
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from src.controllers.User import User

from src.routes.utils.verify_token import token_required

app,db = server.app,server.db

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'Não é possivel executar essa chamada!'})

    users = User.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users':output})

@app.route('/user/<public_id>',methods=['GET'])
@token_required
def get_one_user(current_user,public_id):    
    
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'Usuario não encontrado'})
    
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['email'] = user.email
    user_data['gender'] = user.gender
    user_data['profession'] = user.profession
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user':user_data})

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user,public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'Usuario não encontrado'})

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'],method='sha256')

    user.name = data['name']
    user.email = data['email']
    user.gender = data['gender']
    user.profession = data['profession']
    user.password = hashed_password

    db.session.commit()

    return jsonify({'message':'Usuario alterado corretamente'})

@app.route('/user/<public_id>',methods=['DELETE'])
@token_required
def delete_user(current_user,public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'Usuario não encontrado'})
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'Usuario deletado corretamente!'})

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        jsonify({'message' : 'Ops... Preencha corretamente o Email e a Senha'}),401

    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return jsonify({'message' : 'Ops... Verifique o usuario e a senha'}),401
    
    if check_password_hash(user.password,auth.password):
        token = bytes(jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY']), encoding='utf8')
        return jsonify({'token' : token.decode('UTF-8'),'public_id':user.public_id,'admin':user.admin})

    return jsonify({'message' : 'Ops... Senha incorreta!'}),401

@app.route('/register',methods=['POST'])
def register():
    data = request.get_json()  
    user = User.query.filter_by(email=data['email']).first()    
    if user:
        return jsonify({'message' : 'Ops... Aparentemente esse email ja esta cadastrado na base de dados'}),409
    
    if not data['name'] or not data['email']:
        return jsonify({'message' : 'Ops... Aparentemente existem campos a ser preencidos!'}),409
      
    hashed_password = generate_password_hash(data['password'],method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), 
                    name=data['name'],
                    email=data['email'],
                    gender=data['gender'],
                    profession=data['profession'],
                    password=hashed_password,
                    admin=False)
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'Usuario Criado corretamente!'})
