from flask import  jsonify
from src.service.instance import server

from src.controllers.Airline import Airline

app,db = server.app,server.db

@app.route('/Airline', methods=['GET'])
def get_all_airline():

    airlines = Airline.query.all()
    output = []

    for airline in airlines:
        airline_data = {}
        airline_data['public_id'] = airline.public_id
        airline_data['user_id'] = airline.user_id
        airline_data['whatsapp'] = airline.whatsapp
        airline_data['nome_site'] = airline.nome_site
        airline_data['mensagemPrincpal'] = airline.mensagemPrincpal
        airline_data['mensagemSecundaria'] = airline.mensagemSecundaria
        airline_data['mensagemBotao'] = airline.mensagemBotao
        airline_data['facebook'] = airline.facebook
        airline_data['instagram'] = airline.instagram
        airline_data['logo'] = airline.logo

        output.append(airline_data)

    return jsonify({'airlines':output})

@app.route('/Airline/<nome_site>', methods=['GET'])
def get_airline(nome_site):

    airline = Airline.query.filter_by(nome_site=nome_site).first()
    if not airline:
        return jsonify({'message':'Empresa não encontrada', 'codigo' : 0})

    airline_data = {}
    airline_data['public_id'] = airline.public_id
    airline_data['user_id'] = airline.user_id
    airline_data['whatsapp'] = airline.whatsapp
    airline_data['nome_site'] = airline.nome_site
    airline_data['mensagemPrincpal'] = airline.mensagemPrincpal
    airline_data['mensagemSecundaria'] = airline.mensagemSecundaria
    airline_data['mensagemBotao'] = airline.mensagemBotao
    airline_data['facebook'] = airline.facebook
    airline_data['instagram'] = airline.instagram
    airline_data['logo'] = airline.logo

    return jsonify({'airline':airline_data})