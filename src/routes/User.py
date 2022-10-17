from cmath import log
from flask import request, jsonify, redirect
from src.service.instance import server
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from src.service.config import domain

from src.controllers.User import User

from src.routes.utils.verify_token import token_required

app,db = server.app,server.db

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    users = User.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.nome
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users':output})

@app.route('/AlterPhoto', methods=['PUT'])
@token_required
def AlterPhoto(current_user):   
    try:
        user = User.query.filter_by(public_id=current_user.public_id).first()
        if not user:
            return jsonify({'message':'Usuario não encontrado'})
        
        user.photo = request.get_json()

        db.session.commit()       
    except Exception as e:
        return e 

    return 'sucess'

@app.route('/current_user',methods=['GET'])
@token_required
def current_user(current_user):    
    try:
        user = User.query.filter_by(public_id=current_user.public_id).first()
        if not user:
            return jsonify({'message':'Usuario não encontrado'})
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['nome'] = user.nome
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['ddi'] = user.ddi
        user_data['phone'] = user.phone 
        user_data['photo'] = user.photo 
        user_data['cpf_cnpj'] = user.cpf_cnpj
        user_data['genero'] = user.genero
        user_data['profissao'] = user.profissao
        user_data['data_nascimento'] = user.data_nascimento    
        user_data['session_id'] = user.session_id

        return jsonify({'user':user_data})        
    except Exception as e:
        return e    

@app.route('/user', methods=['PUT'])
@token_required
def promote_user(current_user):
    user = User.query.filter_by(public_id=current_user.public_id).first()
    if not user:
        return jsonify({'message':'Usuario não encontrado'})
      
    user.nome = request.form['nome'] 
    user.email = request.form['email'] 
    user.ddi = request.form['ddi'] 
    user.phone  = request.form['phone'] 
    user.cpf_cnpj = request.form['cpf_cnpj'] 
    user.genero = request.form['genero'] 
    user.profissao = request.form['profissao'] 
    user.data_nascimento = request.form['data_nascimento'] 

    db.session.commit()

    return jsonify({'message':'Usuario alterado corretamente'})

@app.route('/user',methods=['DELETE'])
@token_required
def delete_user(current_user):
    user = User.query.filter_by(public_id=current_user.public_id).first()
    if not user:
        return jsonify({'message':'Usuario não encontrado'})
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'Usuario deletado corretamente!'})

@app.route('/login', methods=['POST'])
def login():    
    if not request.form['email'] or not request.form['password']:
        return redirect(domain()+"login?message=Ops... Preencha corretamente o Email e a Senha")

    user = User.query.filter_by(email=request.form['email']).first()
    if not user:
        return redirect(domain()+"login?message=Ops... Verifique o usuario e a senha")
    
    if check_password_hash(user.password,request.form['password']):
        token = jwt.encode({'public_id' : user.public_id}, app.config['SECRET_KEY'])
        
        return redirect(domain()+"?token="+str(token))

    return redirect(domain()+"login?message=Ops... Senha incorreta!")

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
