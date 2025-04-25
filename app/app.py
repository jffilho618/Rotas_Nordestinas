from flask import Flask, render_template, redirect, url_for, request, flash
from flask import session

from models import db, Usuario, Feedback


app = Flask(__name__, template_folder='templates', static_folder='static')

# Configurações do app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'segredo'

# Inicializa o banco de dados
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.verificar_senha(senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            flash(f'Bem-vindo(a), {usuario.nome}!', 'success')
            return redirect(url_for('main'))  # redirecione para a rota desejada
        else:
            flash('Email ou senha incorretos.', 'danger')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']
        
        if senha != confirmar_senha:
            flash('As senhas não coincidem.', 'warning')
            return redirect(url_for('cadastro'))
        
        if Usuario.query.filter_by(email=email).first():
            flash('Este email já está cadastrado.', 'danger')
            return redirect(url_for('cadastro'))
        
        novo_usuario = Usuario(nome=nome, email=email)
        novo_usuario.set_senha(senha)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')        

@app.before_request
def verificar_autenticacao():
    rotas_liberadas = ['home', 'login', 'cadastro', 'static']
    
    if request.endpoint not in rotas_liberadas and 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))


@app.context_processor
def inject_back_button():
    def get_back_url():
        if request.path == '/recife':
            return '/main'
        elif request.path in ['/como-chegar', '/atividades', '/pontos-turisticos', '/dicas']:
            return '/recife'
        else:
            return '/main'
    return dict(get_back_url=get_back_url)

@app.route('/cidade/<nome_cidade>', methods=['GET', 'POST'])
def cidade(nome_cidade):
    feedbacks = Feedback.query.filter_by(cidade=nome_cidade).order_by(Feedback.data.desc()).all()
    
    # Se o usuário enviar um novo feedback
    if request.method == 'POST':
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para enviar feedback.', 'warning')
            return redirect(url_for('login'))
        
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        usuario_id = session['usuario_id']
        
        novo_feedback = Feedback(
            cidade=nome_cidade,
            usuario_id=usuario_id,
            titulo=titulo,
            descricao=descricao
        )
        db.session.add(novo_feedback)
        db.session.commit()
        flash('Feedback enviado com sucesso!', 'success')
        return redirect(url_for('cidade', nome_cidade=nome_cidade))
    
    flash('não foi possível carregar os feedbacks', 'warning')
    return render_template('estados/pernambuco/caruaru.html', cidade=nome_cidade, feedbacks=feedbacks)


@app.route('/')
def home():
    # Redireciona para a página index
    return render_template('index.html')

@app.route('/main')
def main():
    # Página principal após o index
    return render_template('main.html')

@app.route('/recife')
def recife():
    # Página da cidade de Recife
    return render_template('global/recife.html')

@app.route('/global/<template_name>')
def global_template(template_name):
    try:
        # Adiciona a extensão .html se não estiver presente
        if not template_name.endswith('.html'):
            template_name += '.html'
        return render_template(f'global/{template_name}')
    except Exception as e:
        print(f"Erro ao carregar template {template_name}: {str(e)}")
        return f"Erro ao carregar template {template_name}", 500


@app.route('/<path:template_path>')
def render_dynamic_template(template_path):
    try:
        if not template_path.endswith('.html'):
            template_path += '.html'
        return render_template(template_path)
    except Exception as e:
        print(f"Erro ao carregar template {template_path}: {str(e)}")
        return f"Erro ao carregar template {template_path}", 500

@app.route('/como-chegar/<estado>/<cidade>')
def como_chegar(estado, cidade):
    try:
        return render_template('global/como_chegar.html', estado=estado, cidade=cidade)
    except Exception as e:
        print(f"Erro ao carregar página de como chegar: {str(e)}")
        return f"Erro ao carregar página de como chegar", 500

@app.route('/pontos-turisticos/<estado>/<cidade>')
def pontos_turisticos(estado, cidade):
    try:
        return render_template('global/pontos_turisticos.html', estado=estado, cidade=cidade)
    except Exception as e:
        print(f"Erro ao carregar pontos turísticos: {str(e)}")
        return "Erro ao carregar página de pontos turísticos", 500

@app.route('/atividades/<estado>/<cidade>')
def atividades(estado, cidade):
    try:
        return render_template('global/atividades.html', estado=estado, cidade=cidade)
    except Exception as e:
        print(f"Erro ao carregar atividades: {str(e)}")
        return "Erro ao carregar página de atividades", 500

@app.route('/dicas/<estado>/<cidade>')
def dicas(estado, cidade):
    try:
        return render_template('global/dicas.html', estado=estado, cidade=cidade)
    except Exception as e:
        print(f"Erro ao carregar dicas: {str(e)}")
        return "Erro ao carregar página de dicas", 500


@app.route('/modais/<path:modal_path>')
def modal_template(modal_path):
    # Para servir os modais
    return render_template(f'modais/{modal_path}.html')

# Rotas para os componentes reutilizáveis
@app.route('/components/<component_name>')
def component(component_name):
    try:
        return render_template(f'global/{component_name}')
    except Exception as e:
        print(f"Erro ao carregar componente {component_name}: {str(e)}")
        return f"Erro ao carregar componente {component_name}", 500
    


if __name__ == '__main__':
    app.run(debug=True)