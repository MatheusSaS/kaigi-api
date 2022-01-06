from flask import request, jsonify
from src.service.instance import server
from src.routes.utils.verify_token import token_required
from src.controllers.Admin import Subject,Category
import uuid

app,db = server.app,server.db

""" --- End Point subject --- """
@app.route('/admin/subject', methods=['GET'])
@token_required
def get_all_subject(current_user):
    
    subjects = Subject.query.all()
    output = []

    for subject in subjects:
        subject_Data = {}
        subject_Data['public_id'] = subject.public_id
        subject_Data['description'] = subject.description
        output.append(subject_Data)

    return jsonify({'subject':output})

@app.route('/admin/subject/<public_id>', methods=['PUT'])
@token_required
def promote_subject(current_user,public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Não é possivel executar essa chamada!'})

    subject = Subject.query.filter_by(public_id=public_id).first()
    if not subject:
        return jsonify({'message':'Assunto não encontrado'})

    data = request.get_json()

    subject.description = data['description']

    db.session.commit()

    return jsonify({'message':'Assunto alterado corretamente'})

@app.route('/admin/subject/<public_id>',methods=['DELETE'])
@token_required
def delete_subject(current_user,public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Não é possivel executar essa chamada!'})

    subject = Subject.query.filter_by(public_id=public_id).first()
    if not subject:
        return jsonify({'message':'Assunto não encontrado'})
    
    db.session.delete(subject)
    db.session.commit()
    return jsonify({'message':'Assunto deletado corretamente!'})

@app.route('/admin/subject',methods=['POST'])
@token_required
def create_subject(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Não é possivel executar essa chamada!'})
    
    data = request.get_json()    
    if not data['description']:
        return jsonify({'message' : 'Ops... Aparentemente existem campos a ser preencidos!'}),409
      
    new_subject = Subject(public_id=str(uuid.uuid4()), 
                    description=data['description'])
    
    db.session.add(new_subject)
    db.session.commit()
    return jsonify({'message':'Assunto Criado corretamente!'})

""" --- End Point category --- """
@app.route('/category', methods=['GET'])
def get_all_category():
    
    categories = Category.query.all()
    output = []

    for category in categories:
        subject_Data = {}
        subject_Data['public_id'] = category.public_id
        subject_Data['description'] = category.description
        subject_Data['image'] = category.image
        output.append(subject_Data)

    return jsonify({'category':output})

@app.route('/admin/category/<public_id>', methods=['PUT'])
@token_required
def promote_category(current_user,public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Não é possivel executar essa chamada!'})

    categories = Category.query.filter_by(public_id=public_id).first()
    if not categories:
        return jsonify({'message':'Assunto não encontrado'})

    data = request.get_json()
    print(data)
    categories.description = data['description']
    categories.image = data['image']

    db.session.commit()

    return jsonify({'message':'Categoria alterada corretamente'})

@app.route('/admin/category/<public_id>',methods=['DELETE'])
@token_required
def delete_category(current_user,public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Não é possivel executar essa chamada!'})

    categories = Category.query.filter_by(public_id=public_id).first()
    if not categories:
        return jsonify({'message':'Assunto não encontrado'})
    
    db.session.delete(categories)
    db.session.commit()
    return jsonify({'message':'Categoria deletada corretamente!'})

@app.route('/admin/category',methods=['POST'])
@token_required
def create_category(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Não é possivel executar essa chamada!'})
    
    data = request.get_json()  
    if not data['description'] or not data['image']:
        return jsonify({'message' : 'Ops... Aparentemente existem campos a ser preencidos!'}),409
      
    new_category = Category(public_id=str(uuid.uuid4()), 
                            description=data['description'],
                            image=data['image'])
    
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message':'Categoria Criado corretamente!'})