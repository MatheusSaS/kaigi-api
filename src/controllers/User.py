from src.service.instance import server
from sqlalchemy_utils import PhoneNumber
from sqlalchemy.orm import composite
from datetime import datetime

db = server.db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    nome = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    ddi = db.Column(db.Unicode(8))
    cpf_cnpj = db.Column(db.String(18))
    password = db.Column(db.String(80))
    genero = db.Column(db.String(80))    
    profissao = db.Column(db.String(50))
    data_nascimento = db.Column(db.Date())
    admin = db.Column(db.Boolean)
    phone = db.Column(db.String(20))
    data_criacao = db.Column(db.Date(), default=datetime.now)
    session_id = db.Column(db.String(225))
    photo = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.name

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.public_id'))
    pais = db.Column(db.String(80))
    estado = db.Column(db.String(120))
    cidade = db.Column(db.Unicode(120))
    cep = db.Column(db.String(25))
    logradouro = db.Column(db.String(80))
    numero = db.Column(db.String(80))    
    complemento = db.Column(db.String(50))
    bairro = db.Column(db.String(80))
    def __repr__(self):
        return '<Endereco %r>' % self.name

class Cancel_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    email = db.Column(db.String(120), unique=True)   
    data_criacao = db.Column(db.Date(), default=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.name        
     

db.create_all()
