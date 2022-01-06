from enum import unique
from src.service.instance import server

db = server.db

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    description = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Subject %r>' % self.description

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    description = db.Column(db.String(80), nullable=False)
    image = db.Column(db.VARCHAR)

    def __repr__(self):
        return '<Category %r>' % self.description

db.create_all()
