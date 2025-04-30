from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
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
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    usuario_nome = request.form.get('usuario')
    senha = request.form.get('senha')
    
    usuario = Usuario.query.filter_by(usuario=usuario_nome).first()
    
    if usuario and usuario.verificar_senha(senha):
        session['usuario_id'] = usuario.id
        session['usuario_nome'] = usuario.nome
        session['usuario_role'] = usuario.role
        return jsonify(success=True, mensagem=f'Bem-vindo(a), {usuario.nome}!')
    else:
        return jsonify(success=False, mensagem='Usuário ou senha incorretos.')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        data = request.get_json()
    
        nome = data.get('nome')
        sobrenome = data.get('sobrenome')
        email = data.get('email')
        telefone = data.get('telefone')
        usuario = data.get('usuario')
        senha = data.get('senha')
        
        if Usuario.query.filter_by(usuario=usuario).first():
            flash('Este nome de usuário já está cadastrado.', 'danger')
            return redirect(url_for('index'))
        
        novo_usuario = Usuario(nome=nome, sobrenome=sobrenome, email=email, telefone=telefone, usuario=usuario)
        novo_usuario.set_senha(senha)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('home'))
    
    return render_template('index.html')        

@app.before_request
def verificar_autenticacao():
    rotas_liberadas = ['home', 'login', 'cadastro', 'static', 'load_modal']
    
    if request.endpoint not in rotas_liberadas and 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('home'))


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
    if request.method == 'POST':
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para enviar feedback.', 'warning')
            return redirect(url_for('main'))

        titulo = request.form['titulo']
        descricao = request.form['descricao']
        usuario_id = session['usuario_id']
        estado = request.form['estado']

        novo_feedback = Feedback(
            cidade=nome_cidade,
            usuario_id=usuario_id,
            titulo=titulo,
            descricao=descricao
        )
        db.session.add(novo_feedback)
        db.session.commit()
        flash('Feedback enviado com sucesso!', 'success')

        return redirect(url_for('cidade', nome_cidade=nome_cidade, estado=estado))
    
    estado = request.args.get('estado', 'padrao')  # usa query param se vier pela URL
    feedbacks = Feedback.query.filter_by(cidade=nome_cidade).order_by(Feedback.data.desc()).all()

    return render_template(f'estados/{estado}/{nome_cidade}.html', cidade=nome_cidade, estado=estado, feedbacks=feedbacks)

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/')
def home():
    # Redireciona para a página index
    return render_template('index.html')

@app.route('/main')
def main():
    usuario = None
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
    return render_template('main.html', usuario=usuario)

@app.route('/deletar_feedback/<int:feedback_id>', methods=['POST'])
def deletar_feedback(feedback_id):
    if session.get('usuario_role') != 'admin':
        flash('Apenas administradores podem excluir feedbacks.', 'danger')
        return redirect(url_for('main'))

    feedback = Feedback.query.get_or_404(feedback_id)
    cidade = feedback.cidade

    estado = request.args.get('estado', 'pernambuco')

    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback excluído com sucesso!', 'success')

    return redirect(url_for('cidade', nome_cidade=cidade, estado=estado))

@app.route('/favoritos')
def favoritos():
    usuario = None
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
    return render_template('global/favoritos.html', usuario=usuario)

@app.route('/perfil')
def perfil():
    usuario = None
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
    return render_template('global/perfil.html', usuario=usuario)

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
def load_modal(modal_path):
    print(f"Carregando modal: {modal_path}")
    return render_template(f"modais/{modal_path}.html")


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