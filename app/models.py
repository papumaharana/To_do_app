from app import db


# Creating table using pythonic way
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(50), default = 'pending')

    user_id = db.Column(db.Integer, db.ForeignKey('register.id'), nullable=False)
    

class Register(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(30),  nullable = False)

    task = db.relationship('Task', backref='register', lazy=True)

    