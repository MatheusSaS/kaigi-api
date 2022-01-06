from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

class Server():
    def __init__(self, ):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'kaigitcc2021'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apidb.db'
        self.app.config['CORS_HEADERS'] = 'Content-Type'
        self.db = SQLAlchemy(self.app)
        CORS(self.app)

    def run(self, ):
        self.app.run(debug=True)

server = Server()