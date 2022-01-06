from src.service.instance import server

db = server.db

class TypeTicket (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Type_Ticket %r>' % self.public_id

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_type_ticket = db.Column(db.Integer, db.ForeignKey('type_ticket.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.public_id'))
    public_id = db.Column(db.String(50),unique=True)
    ticket_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)    
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    initial_date_time = db.Column(db.DateTime, nullable=False) 
    final_date_time = db.Column(db.DateTime, nullable=False)
    amount_min = db.Column(db.Integer, nullable=False)
    amount_max = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))

    half = db.Column(db.Boolean)
    half_description = db.Column(db.String(200))
    half_amount = db.Column(db.Integer)
    half_price = db.Column(db.Float)
    half_total = db.Column(db.Float)

    def __repr__(self):
        return '<Ticket %r>' % self.public_id

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_type_event = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.public_id'))
    public_id = db.Column(db.String(50),unique=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.VARCHAR)
    subject = db.Column(db.Integer, db.ForeignKey('subject.public_id'))   
    category = db.Column(db.Integer, db.ForeignKey('category.public_id'))
    initial_date_time = db.Column(db.DateTime, nullable=False)  
    final_date_time = db.Column(db.DateTime, nullable=False)  
    description = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(200))
    
    local = db.Column(db.String(100))
    address = db.Column(db.String(100))
    location_name = db.Column(db.String(100))
    cep = db.Column(db.String(100))
    road = db.Column(db.String(100))
    number = db.Column(db.Integer)
    complement = db.Column(db.String(100))
    district = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))

    def __repr__(self):
        return '<Event %r>' % self.public_id

class TicketEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    public_id = db.Column(db.String(50),unique=True)
    ticket_public_id = db.Column(db.String(50), db.ForeignKey('ticket.public_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.public_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.public_id'))

    def __repr__(self):
        return '<TicketEvent %r>' % self.public_id

db.create_all()