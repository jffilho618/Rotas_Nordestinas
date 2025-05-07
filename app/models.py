from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    usuario = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
        
    # Relacionamentos
    feedbacks = db.relationship('Feedback', backref='autor', lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cidade = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    titulo = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Feedback {self.titulo}>'