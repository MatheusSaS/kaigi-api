from flask import request, jsonify
from src.service.instance import server
import uuid
from dateutil import parser
import requests

from src.controllers.Events import Ticket,Event,TicketEvent
from src.controllers.Admin import Category

from src.routes.utils.verify_token import token_required

app,db = server.app,server.db

@app.route('/ticket', methods=['GET'])
@token_required
def get_all_ticket(current_user):

    tickets = Ticket.query.filter_by(user_id=current_user.public_id).all()
    output = []

    for ticket in tickets:
        ticket_data = {}
        ticket_data['id_type_ticket'] = ticket.id_type_ticket
        ticket_data['user_id'] = ticket.user_id
        ticket_data['public_id'] = ticket.public_id
        ticket_data['ticket_name'] = ticket.ticket_name
        ticket_data['amount'] = ticket.amount
        ticket_data['price'] = ticket.price
        ticket_data['total'] = ticket.total
        ticket_data['initial_date_time'] = ticket.initial_date_time
        ticket_data['final_date_time'] = ticket.final_date_time
        ticket_data['amount_min'] = ticket.amount_min
        ticket_data['amount_max'] = ticket.amount_max
        ticket_data['description'] = ticket.description

        ticket_data['half'] = ticket.half
        ticket_data['half_description'] = ticket.half_description
        ticket_data['half_amount'] = ticket.half_amount
        ticket_data['half_price'] = ticket.half_price
        ticket_data['half_total'] = ticket.half_total

        output.append(ticket_data)

    return jsonify({'tickets':output})

@app.route('/ticket/<public_id>',methods=['GET'])
@token_required
def get_one_ticket(current_user,public_id):    
    
    ticket = Ticket.query.filter_by(public_id=public_id).first()
    if not ticket:
        return jsonify({'message':'Ingresso não encontrado'})
    
    ticket_data = {}
    ticket_data['id_type_ticket'] = ticket.id_type_ticket
    ticket_data['user_id'] = ticket.user_id
    ticket_data['ticket_name'] = ticket.ticket_name
    ticket_data['public_id'] = ticket.public_id
    ticket_data['amount'] = ticket.amount
    ticket_data['price'] = ticket.price
    ticket_data['total'] = ticket.total
    ticket_data['initial_date_time'] = ticket.initial_date_time
    ticket_data['final_date_time'] = ticket.final_date_time
    ticket_data['amount_min'] = ticket.amount_min
    ticket_data['amount_max'] = ticket.amount_max
    ticket_data['description'] = ticket.description

    ticket_data['half'] = ticket.half
    ticket_data['half_description'] = ticket.half_description
    ticket_data['half_amount'] = ticket.half_amount
    ticket_data['half_price'] = ticket.half_price
    ticket_data['half_total'] = ticket.half_total

    return jsonify({'ticket':ticket_data})

@app.route('/ticket/<public_id>', methods=['PUT'])
@token_required
def promote_ticket(current_user,public_id):
    ticket = Ticket.query.filter_by(public_id=public_id).first()
    if not ticket:
        return jsonify({'message':'Ingresso não encontrado'})

    data = request.get_json()

    data_obj_initial = parser.parse(data['initial_date_time'])
    data_obj_final = parser.parse(data['final_date_time'])

    ticket.ticket_name = data['ticket_name']
    ticket.amount = data['amount']
    ticket.price = data['price']
    ticket.total = data['total']
    ticket.initial_date_time = data_obj_initial
    ticket.final_date_time = data_obj_final
    ticket.amount_min = data['amount_min']
    ticket.amount_max = data['amount_max']
    ticket.description = data['description']

    ticket.half = data['half']
    ticket.half_amount = data['half_amount']
    ticket.half_price = data['half_price']
    ticket.half_total = data['half_total'] 
    ticket.half_description = data['half_description'] 

    db.session.commit()

    return jsonify({'message':'Ingresso alterado corretamente'})

@app.route('/ticket/<public_id>',methods=['DELETE'])
@token_required
def delete_ticket(current_user,public_id):
    ticket = Ticket.query.filter_by(public_id=public_id).first()
    if not ticket:
        return jsonify({'message':'Ingresso não encontrado'})
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'message':'Ingresso deletado corretamente!'})

@app.route('/ticket',methods=['POST'])
def create_ticket():
    data = request.get_json()  
    if not data['ticket_name'] or not data['amount']  or not data['ticket_name'] or not data['initial_date_time'] or not data['final_date_time'] or not data['amount_min'] or not data['amount_max'] or not data['description']:        
        return jsonify({'message' : 'Ops... Aparentemente existem campos a ser preencidos!'}),409

    data_obj_initial = parser.parse(data['initial_date_time'])
    data_obj_final = parser.parse(data['final_date_time'])
    
    new_ticket = Ticket(public_id=str(uuid.uuid4()),
                    id_type_ticket=data['id_type_ticket'],
                    user_id=data['user_id'],
                    ticket_name=data['ticket_name'],
                    amount=data['amount'],
                    price=data['price'],
                    total=data['total'],
                    initial_date_time= data_obj_initial ,
                    final_date_time= data_obj_final,
                    amount_min=data['amount_min'],
                    amount_max=data['amount_max'],
                    description=data['description'],
                    half=data['half'],
                    half_description=data['half_description'],
                    half_amount=data['half_amount'],
                    half_price=data['half_price'],
                    half_total=data['half_total'])
    
    db.session.add(new_ticket)
    db.session.commit()
    return jsonify({'message':'Ingresso Criado corretamente!'})

    """ -------------- Events ------------------"""

@app.route('/event', methods=['GET'])
def get_all_events():
    events = Event.query.all()
    output = []

    for event in events:
        event_data = {}
        event_data['name'] = event.name
        event_data['public_id'] = event.public_id
        event_data['image'] = event.image 
        event_data['subject'] = event.subject
        event_data['category'] = event.category
        event_data['initial_date'] = event.initial_date_time
        event_data['final_date'] = event.final_date_time
        event_data['description'] = event.description
        event_data['platform'] = event.platform
        event_data['local'] = event.local
        event_data['location_name'] = event.location_name
        event_data['cep'] = event.cep
        event_data['road'] = event.road
        event_data['number'] = event.number
        event_data['complement'] = event.complement
        event_data['district'] = event.district
        event_data['city'] = event.city
        event_data['state'] = event.state

        output.append(event_data)

    return jsonify({'events':output})

@app.route('/myEvent/<public_id>', methods=['GET'])
@token_required
def get_my_events(current_user,public_id):  
    print(public_id)
    events = Event.query.filter_by(user_id=public_id).all()
    print('aaaaaaaaaaaaaaaaaaaaaaaaa')
    print(events)
    output = []

    for event in events:
        event_data = {}
        event_data['name'] = event.name        
        event_data['image'] = event.image 
        event_data['subject'] = event.subject
        event_data['category'] = event.category
        event_data['initial_date'] = event.initial_date_time
        event_data['final_date'] = event.final_date_time
        event_data['description'] = event.description
        event_data['platform'] = event.platform
        event_data['local'] = event.local
        event_data['location_name'] = event.location_name
        event_data['cep'] = event.cep
        event_data['road'] = event.road
        event_data['number'] = event.number
        event_data['complement'] = event.complement
        event_data['district'] = event.district
        event_data['city'] = event.city
        event_data['state'] = event.state
        event_data['public_id'] = event.public_id

        output.append(event_data)

    return jsonify({'events':output})

@app.route('/event/<public_id>',methods=['GET'])
def get_one_event(public_id):        
    event = Event.query.filter_by(public_id=public_id).first()
    if not event:
        return jsonify({'message':'Ingresso não encontrado'})
    
    event_data = {}
    event_data['name'] = event.name
    event_data['image'] = event.image 
    event_data['subject'] = event.subject
    event_data['category'] = event.category
    event_data['initial_date'] = event.initial_date_time
    event_data['final_date'] = event.final_date_time
    event_data['description'] = event.description
    event_data['platform'] = event.platform
    event_data['local'] = event.local
    event_data['location_name'] = event.location_name
    event_data['cep'] = event.cep
    event_data['road'] = event.road
    event_data['number'] = event.number
    event_data['complement'] = event.complement
    event_data['district'] = event.district
    event_data['city'] = event.city
    event_data['state'] = event.state
    event_data['id_type_event'] = event.id_type_event

    return jsonify({'event':event_data})

@app.route('/event/<public_id>', methods=['PUT'])
@token_required
def promote_event(current_user,public_id):
    event = Event.query.filter_by(public_id=public_id).first()
    if not event:
        return jsonify({'message':'Evento não encontrado'})

    data = request.get_json()

    data_obj_initial = parser.parse(data['initial_date'])
    data_obj_final = parser.parse(data['final_date'])

    event.name = data['name']
    event.image = data['image']
    event.subject = data['subject']
    event.category = data['category']
    event.initial_date_time = data_obj_initial
    event.final_date_time = data_obj_final
    event.description = data['description']
    event.platform = data['platform']
    event.local = data['local']
    event.location_name = data['location_name']
    event.cep = data['cep'] 

    db.session.commit()

    return jsonify({'message':'Ingresso alterado corretamente'})

@app.route('/event/<public_id>',methods=['DELETE'])
@token_required
def delete_event(current_user,public_id):
    event = Event.query.filter_by(public_id=public_id).first()
    if not event:
        return jsonify({'message':'Ingresso não encontrado'})

    db.session.delete(event)
    db.session.commit()
    return jsonify({'message':'Ingresso deletado corretamente!'})

@app.route('/event',methods=['POST'])
def create_event():
    data = request.get_json()  
    print(data)
    if not data['name'] or not data['subject']  or not data['category']:        
        return jsonify({'message' : 'Ops... Aparentemente existem campos a ser preencidos!'}),409        

    data_obj_initial = parser.parse(data['initial_date'])
    data_obj_final = parser.parse(data['final_date'])
    
    public_id=str(uuid.uuid4())
    new_event = Event(public_id=public_id,
                    id_type_event=data['id_type_event'],
                    user_id=data['user_id'],
                    name=data['name'],
                    image=data['image'],
                    subject=data['subject'],
                    category=data['category'],
                    initial_date_time=data_obj_initial,
                    final_date_time= data_obj_final ,
                    description=data['description'],
                    platform=data['platform'],
                    local=data['local'],
                    address=data['address'],
                    location_name=data['location_name'],
                    cep=data['cep'],
                    road=data['road'],
                    number=data['number'],
                    complement=data['complement'],
                    district=data['district'],
                    city=data['city'],
                    state=data['state'],)
            
    for ticket in data['ticket_id']:
        value = ''
        value = TicketEvent.query.filter_by(ticket_public_id=ticket,event_id=public_id).first()
        if not value:
            link_ticket = TicketEvent(public_id=str(uuid.uuid4()),
                                       ticket_public_id=ticket,
                                       event_id=public_id,
                                       user_id=data['user_id'])
            db.session.add(link_ticket)
            db.session.commit()
    
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message':'Ingresso Criado corretamente!'})   



@app.route('/city',methods=['GET'])
def get_city():
    events = Event.query.group_by(Event.city).all()
    output = []

    for city in events:
        city_data = {}
        city_data['city'] = city.city

        output.append(city_data)

    return jsonify({'city':output})


@app.route('/viacep/<cep>',methods=['GET'])
def viacep(cep):
    request = requests.get('https://viacep.com.br/ws/{}/json/'.format(cep))
    address_data = request.json()
    print(address_data)
    return jsonify({'result':address_data})

@app.route('/category/<name_category>',methods=['GET'])
def category(name_category):

    category_id = Category.query.filter_by(description = name_category).first()    
    events = Event.query.filter_by(category = category_id.public_id).all()

    if not events:
        return jsonify({'message':'Evento não encontrado'})
    
    output = []

    for event in events:
        event_data = {}
        event_data['name'] = event.name
        event_data['public_id'] = event.public_id
        event_data['image'] = event.image 
        event_data['subject'] = event.subject
        event_data['category'] = event.category
        event_data['initial_date'] = event.initial_date_time
        event_data['final_date'] = event.final_date_time
        event_data['description'] = event.description
        event_data['platform'] = event.platform
        event_data['local'] = event.local
        event_data['location_name'] = event.location_name
        event_data['cep'] = event.cep
        event_data['road'] = event.road
        event_data['number'] = event.number
        event_data['complement'] = event.complement
        event_data['district'] = event.district
        event_data['city'] = event.city
        event_data['state'] = event.state

        output.append(event_data)

    return jsonify({'category':output})

    



