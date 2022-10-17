from flask import request,  redirect, jsonify, url_for
from werkzeug.security import generate_password_hash
from src.service.instance import server
from src.service.config import domain,urlapi
from src.controllers.User import User, Cancel_User
from src.controllers.Airline import Airline
import uuid
from src.routes.utils.verify_token import token_required
import stripe
from src.routes.utils.verify_token import token_required

stripe.api_key = urlapi()
app,db = server.app,server.db

def Create_Arline(public_id,nome_site):        
    new_arline = Airline(public_id=str(uuid.uuid4()),
                        user_id=public_id,
                        nome_site=nome_site,
                        mensagemPrincpal='Bem-Vindo!',
                        mensagemSecundaria='O mundo é um livro, e aqueles que não viajam leem apenas uma página',
                        mensagemBotao='Enviar cotação')

    db.session.add(new_arline)
    db.session.commit()      
    return '' 

def Create_Cancel_User():
    if not request.form['password'] or not request.form['email']:
        return jsonify({'message' : 'Ops... Aparentemente existem campos a ser preencidos!'}),409

    user = Cancel_User.query.filter_by(email=request.form['email']).first()     
    if not user:        
        new_user = Cancel_User(public_id=str(uuid.uuid4()), 
                        email=request.form['email'],)
    
        db.session.add(new_user)
        db.session.commit()  
    return ''   

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():    
    try:
        user = User.query.filter_by(email=request.form['email']).first()    
        if user:
            return redirect(domain()+"register?message=Ops... Aparentemente esse email ja esta cadastrado")

        arline = Airline.query.filter_by(nome_site=request.form['nome_site']).first()     
        if arline:        
            return redirect(domain()+"register?message=Ops... O nome do site fornecido ja está em uso")

        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            return redirect(domain()+"register?message=Ops... Aparentemente esse email ja esta cadastrado")

        email = request.form['email']
        nome_site = request.form['nome_site']
        hashed_password = generate_password_hash(request.form['password'],method='sha256')
        
        checkout_session = stripe.checkout.Session.create( 
            customer_email =  request.form['email'],          
            line_items=[
                {
                    'price': request.form['billing'] ,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            
            success_url='http://127.0.0.1:5000/success?session_id={CHECKOUT_SESSION_ID}&email='+email+'&hashed='+hashed_password+'&nome_site='+nome_site ,            
            cancel_url=Create_Cancel_User() +domain()+ 'register',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(e)
        return "Server error", 500         

@app.route('/success', methods=['GET'])
def success():    
    if not request.args.get('email'):
        return jsonify({'message' : 'Ops... Aparentemente existem campos a ser preencidos!'}),409

    public_id=str(uuid.uuid4())   
    nome_site=request.args.get('nome_site') 

    new_user = User(public_id=public_id, 
                    email=request.args.get('email'),
                    password=request.args.get('hashed'),
                    session_id=request.args.get('session_id'),
                    admin=False,)
    
    db.session.add(new_user)
    db.session.commit()

    cancel_user = Cancel_User.query.filter_by(email=request.args.get('email')).first()  
    if cancel_user:
        db.session.delete(cancel_user)
        db.session.commit()

    Create_Arline(public_id,nome_site)
    return redirect(domain()+"login")

@app.route('/create-portal-session', methods=['POST'])
def customer_portal(): 
    checkout_session_id = request.form.get('session_id')
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

    portalSession = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=domain(),
    )
    
    return redirect(portalSession.url, code=303)

@app.route('/webhook', methods=['POST'])
def webhook_received():
    webhook_secret = 'whsec_12345'
    request_data = json.loads(request.data)

    if webhook_secret:
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e

        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    print('event ' + event_type)

    if event_type == 'checkout.session.completed':
        print('🔔 Payment succeeded!')
    elif event_type == 'customer.subscription.trial_will_end':
        print('Subscription trial will end')
    elif event_type == 'customer.subscription.created':
        print('Subscription created %s', event.id)
    elif event_type == 'customer.subscription.updated':
        print('Subscription created %s', event.id)
    elif event_type == 'customer.subscription.deleted':
        print('Subscription canceled: %s', event.id)

    return jsonify({'status': 'success'})


   