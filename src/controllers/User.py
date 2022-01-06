from enum import unique
from src.service.instance import server

db = server.db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(80))
    password = db.Column(db.String(80))
    profession = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User %r>' % self.name

db.create_all()
