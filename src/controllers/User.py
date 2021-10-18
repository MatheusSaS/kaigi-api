from enum import unique
from src.service.instance import server

db = server.db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User %r>' % self.username
db.create_all()
