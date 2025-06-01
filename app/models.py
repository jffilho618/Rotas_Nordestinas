from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    strikes = db.Column(db.Integer, default=0)
    banido = db.Column(db.Boolean, default=False)
    telefone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    usuario = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    feedbacks = db.relationship('Feedback', backref='autor', lazy=True)
    sugestoes = db.relationship('Sugestao', backref='autor', lazy=True)

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
    
class Denuncia(db.Model):
    __tablename__ = 'denuncias'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedbacks.id'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref='denuncias', lazy=True)
    feedback = db.relationship('Feedback', backref='denuncias', lazy=True)

    def __repr__(self):
        return f'<Denuncia de Usuario {self.usuario_id} no Feedback {self.feedback_id}>'

# Nova classe para Sugestões de Rotas
class Sugestao(db.Model):
    __tablename__ = 'sugestoes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    estado = db.Column(db.String(2), nullable=False)  # Sigla do estado (ex: PE, BA)
    cidade = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pendente')  # pendente, aprovada, rejeitada
    
    # Relacionamentos
    pontos_turisticos = db.relationship('PontoTuristico', backref='sugestao', lazy=True, cascade='all, delete-orphan')
    fotos = db.relationship('FotoSugestao', backref='sugestao', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Sugestao {self.cidade}, {self.estado}>'

# Classe para Pontos Turísticos de uma Sugestão
class PontoTuristico(db.Model):
    __tablename__ = 'pontos_turisticos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sugestao_id = db.Column(db.Integer, db.ForeignKey('sugestoes.id'), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    
    def __repr__(self):
        return f'<PontoTuristico {self.nome}>'

# Classe para Fotos de uma Sugestão
class FotoSugestao(db.Model):
    __tablename__ = 'fotos_sugestao'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sugestao_id = db.Column(db.Integer, db.ForeignKey('sugestoes.id'), nullable=False)
    caminho = db.Column(db.String(255), nullable=False)  # Caminho para o arquivo da foto
    legenda = db.Column(db.String(200))  # Legenda opcional para a foto
    
    def __repr__(self):
        return f'<FotoSugestao {self.id} da Sugestao {self.sugestao_id}>'
    
class Favorito(db.Model):
    __tablename__ = 'favoritos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    item_id = db.Column(db.String(50), nullable=False)  # ID único do item (ex: 'atividade1', 'ponto_turistico1')
    tipo = db.Column(db.String(20), nullable=False)  # 'atividade' ou 'ponto_turistico'
    cidade = db.Column(db.String(100), nullable=False)  # Cidade onde está localizado
    nome = db.Column(db.String(200), nullable=False)  # Nome do item
    descricao = db.Column(db.Text, nullable=False)  # Descrição do item
    imagem = db.Column(db.String(255), nullable=False)  # Caminho da imagem
    data_adicionado = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Constraint para evitar duplicatas
    __table_args__ = (db.UniqueConstraint('usuario_id', 'item_id', name='unique_user_item'),)
    
    def __repr__(self):
        return f'<Favorito {self.nome} do Usuario {self.usuario_id}>'
