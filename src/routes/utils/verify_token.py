from flask import request, jsonify
from src.service.instance import server
from functools import wraps
from src.controllers.User import User
import jwt

app = server.app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        def __init__(self, ):
            self.token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']       

        if not token:
            return jsonify({'message' : 'Token não encontrado'}),401
       
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']) 
            current_user = User.query.filter_by(public_id=data['public_id']).first()

        except:
            return jsonify({'message' : 'Ops... Aparentemente você não esta logado!'}),401
      
        return f(current_user, *args, **kwargs)

    return decorated