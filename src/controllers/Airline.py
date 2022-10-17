from src.service.instance import server

db = server.db

class Airline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.public_id'))
    whatsapp = db.Column(db.String(25), )
    nome_site = db.Column(db.String(80), nullable=False,unique=True)
    mensagemPrincpal = db.Column(db.String(225), nullable=False)
    mensagemSecundaria = db.Column(db.String(225))
    mensagemBotao = db.Column(db.String(225))
    facebook = db.Column(db.String(225))
    instagram = db.Column(db.String(225))
    logo = db.Column(db.VARCHAR)


    def __repr__(self):
        return '<Airline %r>' % self.name

db.create_all()
