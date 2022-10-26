from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer,  primary_key=True) # chaves primárias são obrigatórias para o SQLAlchemy
    usuario = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))
    cpf = db.Column(db.String(1000))
    cnpj = db.Column(db.String(1000))


