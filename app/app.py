from datetime import datetime
import os
from sqlite3 import IntegrityError
from werkzeug.utils import secure_filename
from flask import session
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from models import db, Usuario, Feedback, Denuncia, Sugestao, PontoTuristico, FotoSugestao, Favorito


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
        return redirect(url_for('index'))
    
    return render_template('index.html')        

@app.before_request
def verificar_autenticacao():
    rotas_liberadas = ['home', 'login', 'cadastro', 'static', 'load_modal', 'como_chegar', 'atividades', 'pontos_turisticos', 'dicas', 'cidade', 'recife', 'global_template', 'render_dynamic_template', 'main']    

    if request.endpoint not in rotas_liberadas and 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('home'))


@app.context_processor
def inject_global_vars():
    def get_back_url():
        # Seu código existente...
        return '/main'
    
    # Carregar usuário se estiver logado
    usuario = None
    if 'usuario_id' in session:
        try:
            usuario_id = session['usuario_id']
            usuario = Usuario.query.get(usuario_id)
            if not usuario:
                print(f"AVISO: Usuário com ID {usuario_id} não encontrado no banco de dados, mas existe na sessão")
                # Opcionalmente, limpar a sessão inválida
                session.pop('usuario_id', None)
        except Exception as e:
            print(f"ERRO ao carregar usuário: {e}")
            # Limpar a sessão em caso de erro
            session.pop('usuario_id', None)
    
    return dict(get_back_url=get_back_url, usuario=usuario)

@app.context_processor
def inject_user():
    """Injetar o usuário logado em todos os templates"""
    usuario = None
    if 'usuario_id' in session:
        try:
            usuario_id = session['usuario_id']
            usuario = Usuario.query.get(usuario_id)
        except Exception as e:
            print(f"Erro ao carregar usuário: {e}")
            session.pop('usuario_id', None)
    return dict(usuario=usuario)

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

@app.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get(session['usuario_id'])
    
    # Obter sugestões com base no papel do usuário
    if usuario.role == 'admin':
        # Para administradores, obter todas as sugestões agrupadas por status
        sugestoes_pendentes = Sugestao.query.filter_by(status='pendente').all()
        sugestoes_aprovadas = Sugestao.query.filter_by(status='aprovada').all()
        sugestoes_rejeitadas = Sugestao.query.filter_by(status='rejeitada').all()
        
        # Obter feedbacks denunciados e usuários banidos para o painel de admin
        feedbacks_denunciados = db.session.query(Feedback, db.func.count(Denuncia.id).label('num_denuncias'))\
            .join(Denuncia, Denuncia.feedback_id == Feedback.id)\
            .group_by(Feedback.id)\
            .order_by(db.desc('num_denuncias'))\
            .all()
        
        usuarios_banidos = Usuario.query.filter_by(banido=True).all()
        
        return render_template('global/perfil.html', 
                              usuario=usuario, 
                              sugestoes_pendentes=sugestoes_pendentes,
                              sugestoes_aprovadas=sugestoes_aprovadas,
                              sugestoes_rejeitadas=sugestoes_rejeitadas,
                              feedbacks_denunciados=feedbacks_denunciados,
                              usuarios_banidos=usuarios_banidos)
    else:
        # Para usuários comuns, obter apenas suas próprias sugestões
        sugestoes_usuario = Sugestao.query.filter_by(usuario_id=usuario.id).order_by(Sugestao.data_criacao.desc()).all()
        
        return render_template('global/perfil.html', 
                              usuario=usuario, 
                              sugestoes_usuario=sugestoes_usuario)

@app.route('/sugerir_rota', methods=['GET', 'POST'])
def sugerir_rotas():
    
    # Verificar se o usuário está logado
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para sugerir rotas.', 'error')
        return redirect(url_for('login'))
    
    usuario = db.session.get(Usuario, session['usuario_id'])
    
    if request.method == 'POST':
        try:
            # Obter dados básicos do formulário
            estado = request.form.get('estado')
            cidade = request.form.get('cidade')
            descricao = request.form.get('descricao', '')
            
            # Validar campos obrigatórios
            if not estado or not cidade:
                flash('Estado e cidade são campos obrigatórios.', 'error')
                return render_template('global/sugerir_rotas.html', usuario=usuario)
            
            # Criar nova sugestão
            nova_sugestao = Sugestao(
                usuario_id=session['usuario_id'],
                estado=estado,
                cidade=cidade,
                descricao=descricao
            )
            
            db.session.add(nova_sugestao)
            db.session.flush()  # Para obter o ID da sugestão antes do commit
            
            # Processar pontos turísticos
            pontos_turisticos = request.form.getlist('pontos_turisticos[]')
            for ponto in pontos_turisticos:
                if ponto.strip():  # Verificar se não está vazio
                    novo_ponto = PontoTuristico(
                        sugestao_id=nova_sugestao.id,
                        nome=ponto.strip()
                    )
                    db.session.add(novo_ponto)
            
            # Processar fotos
            if 'fotos[]' in request.files:
                fotos = request.files.getlist('fotos[]')
                for foto in fotos:
                    if foto and foto.filename:
                        # Gerar nome único para o arquivo
                        filename = secure_filename(foto.filename)
                        unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                        
                        # Definir o caminho para salvar a foto
                        upload_folder = os.path.join(app.static_folder, 'uploads', 'sugestoes')
                        
                        # Criar o diretório se não existir
                        if not os.path.exists(upload_folder):
                            os.makedirs(upload_folder)
                        
                        # Salvar arquivo
                        foto_path = os.path.join(upload_folder, unique_filename)
                        foto.save(foto_path)
                        
                        # Caminho relativo para armazenar no banco de dados
                        db_path = f"uploads/sugestoes/{unique_filename}"
                        
                        # Criar registro no banco
                        nova_foto = FotoSugestao(
                            sugestao_id=nova_sugestao.id,
                            caminho=db_path
                        )
                        db.session.add(nova_foto)
            
            # Commit das alterações
            db.session.commit()
            flash('Sugestão enviada com sucesso! Obrigado por contribuir.', 'success')
            return redirect(url_for('sugerir_rotas'))
            
        except Exception as e:
            # Rollback em caso de erro
            db.session.rollback()
            flash(f'Erro ao enviar sugestão: {str(e)}', 'error')
            return render_template('global/sugerir_rotas.html', usuario=usuario)

    return render_template('global/sugerir_rotas.html', usuario=usuario)

@app.route('/api/sugestao/<int:sugestao_id>')
def api_sugestao(sugestao_id):
    if 'usuario_id' not in session:
        return jsonify({'error': 'Não autorizado'}), 401
    
    usuario = Usuario.query.get(session['usuario_id'])
    sugestao = Sugestao.query.get_or_404(sugestao_id)
    
    # Verificar permissão: apenas admin ou o próprio usuário pode ver os detalhes
    if usuario.role != 'admin' and sugestao.usuario_id != usuario.id:
        return jsonify({'error': 'Não autorizado'}), 403
    
    # Preparar dados para JSON
    pontos_turisticos = [{'id': pt.id, 'nome': pt.nome} for pt in sugestao.pontos_turisticos]
    fotos = [{'id': foto.id, 'caminho': url_for('static', filename=foto.caminho)} for foto in sugestao.fotos]
    
    return jsonify({
        'id': sugestao.id,
        'autor_id': sugestao.usuario_id,
        'autor_nome': sugestao.autor.nome + ' ' + sugestao.autor.sobrenome,
        'estado': sugestao.estado,
        'cidade': sugestao.cidade,
        'descricao': sugestao.descricao,
        'data_criacao': sugestao.data_criacao.strftime('%d/%m/%Y %H:%M'),
        'status': sugestao.status,
        'pontos_turisticos': pontos_turisticos,
        'fotos': fotos
    })

@app.route('/aprovar_sugestao/<int:sugestao_id>', methods=['POST'])
def aprovar_sugestao(sugestao_id):
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para realizar esta ação.', 'warning')
        return redirect(url_for('home'))
    
    usuario = Usuario.query.get(session['usuario_id'])
    if usuario.role != 'admin':
        flash('Apenas administradores podem aprovar sugestões.', 'warning')
        return redirect(url_for('perfil'))
    
    sugestao = Sugestao.query.get_or_404(sugestao_id)
    sugestao.status = 'aprovada'
    db.session.commit()
    
    flash('Sugestão aprovada com sucesso!', 'success')
    return redirect(url_for('perfil'))

@app.route('/rejeitar_sugestao/<int:sugestao_id>', methods=['POST'])
def rejeitar_sugestao(sugestao_id):
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para realizar esta ação.', 'warning')
        return redirect(url_for('home'))
    
    usuario = Usuario.query.get(session['usuario_id'])
    if usuario.role != 'admin':
        flash('Apenas administradores podem rejeitar sugestões.', 'warning')
        return redirect(url_for('perfil'))
    
    sugestao = Sugestao.query.get_or_404(sugestao_id)
    sugestao.status = 'rejeitada'
    db.session.commit()
    
    flash('Sugestão rejeitada com sucesso!', 'success')
    return redirect(url_for('perfil'))

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
    

@app.route('/denunciar/<int:feedback_id>', methods=['POST'])
def denunciar_feedback(feedback_id):
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para denunciar.', 'warning')
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']
    cidade = request.args.get('cidade')
    estado = request.args.get('estado', 'padrao')

    # Verifica se o usuário já denunciou esse feedback
    denuncia_existente = Denuncia.query.filter_by(usuario_id=usuario_id, feedback_id=feedback_id).first()
    if denuncia_existente:
        flash('Você já denunciou este feedback.', 'info')
    else:
        nova_denuncia = Denuncia(usuario_id=usuario_id, feedback_id=feedback_id)
        db.session.add(nova_denuncia)
        db.session.commit()
        flash('Feedback denunciado com sucesso!', 'success')

    return redirect(url_for('cidade', nome_cidade=cidade, estado=estado))


@app.route('/dar_strike/<int:usuario_id>/<int:feedback_id>', methods=['POST'])
def dar_strike(usuario_id, feedback_id):
    usuario = Usuario.query.get(usuario_id)
    feedback = Feedback.query.get(feedback_id)
    
    # Adiciona um strike ao usuário
    usuario.strikes += 1

    # Verifica se o usuário deve ser banido
    if usuario.strikes >= 3:
        usuario.banido = True
    
    db.session.commit()

    # Remover todas as denúncias relacionadas ao feedback
    denuncias = Denuncia.query.filter_by(feedback_id=feedback_id).all()
    for denuncia in denuncias:
        db.session.delete(denuncia)
    
    # Remover o feedback após os strikes
    db.session.delete(feedback)
    
    db.session.commit()
    
    return redirect(url_for('perfil'))  # Redireciona de volta para o perfil após dar o strike


@app.route('/remover_denuncia/<int:feedback_id>', methods=['POST'])
def remover_denuncia(feedback_id):
    # Remover todas as denúncias do feedback
    denuncias = Denuncia.query.filter_by(feedback_id=feedback_id).all()
    for denuncia in denuncias:
        db.session.delete(denuncia)
    
    db.session.commit()
    
    return redirect(url_for('perfil'))  # Redireciona de volta para o perfil após remover as denúncias

@app.route('/desbanir_usuario/<int:usuario_id>', methods=['POST'])
def desbanir_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        usuario.banido = False
        usuario.strikes = 0  
        db.session.commit()
    return redirect(url_for('perfil'))

@app.route('/atualizar_perfil', methods=['POST'])
def atualizar_perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.get(session['usuario_id'])
    if not usuario:
        return redirect(url_for('login'))

    # Atualiza os dados
    usuario.nome = request.form.get('nome')
    usuario.sobrenome = request.form.get('sobrenome')
    usuario.email = request.form.get('email')
    usuario.telefone = request.form.get('telefone')

    db.session.commit()

    return redirect(url_for('perfil'))

@app.route('/api/favoritos', methods=['GET'])
def get_favoritos():
    """Retorna todos os favoritos do usuário atual"""
    try:
        usuario_id = session['usuario_id']
        favoritos = Favorito.query.filter_by(usuario_id=usuario_id).all()
        favoritos_data = []
        
        for favorito in favoritos:
            favoritos_data.append({
                'id': favorito.id,
                'item_id': favorito.item_id,
                'tipo': favorito.tipo,
                'cidade': favorito.cidade,
                'nome': favorito.nome,
                'descricao': favorito.descricao,
                'imagem': favorito.imagem,
                'data_adicionado': favorito.data_adicionado.isoformat()
            })
        
        return jsonify(favoritos_data), 200
    
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/favoritos', methods=['POST'])
def adicionar_favorito():
    """Adiciona um item aos favoritos"""
    try:
        data = request.get_json()
        usuario_id = session['usuario_id']
        
        # Validação dos dados obrigatórios
        required_fields = ['item_id', 'nome', 'descricao', 'imagem', 'tipo', 'cidade']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verifica se já existe
        favorito_existente = Favorito.query.filter_by(
            usuario_id=usuario_id,
            item_id=data['item_id']
        ).first()
        
        if favorito_existente:
            return jsonify({'error': 'Item já está nos favoritos'}), 409
        
        # Cria novo favorito
        novo_favorito = Favorito(
            usuario_id=usuario_id,
            item_id=data['item_id'],
            tipo=data['tipo'],
            cidade=data['cidade'],
            nome=data['nome'],
            descricao=data['descricao'],
            imagem=data['imagem']
        )
        
        db.session.add(novo_favorito)
        db.session.commit()
        
        return jsonify({
            'message': 'Favorito adicionado com sucesso',
            'favorito_id': novo_favorito.id
        }), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Item já está nos favoritos'}), 409
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/favoritos/<item_id>', methods=['DELETE'])
def remover_favorito(item_id):
    """Remove um item dos favoritos"""
    try:
        usuario_id = session['usuario_id']
        favorito = Favorito.query.filter_by(
            usuario_id=usuario_id,
            item_id=item_id
        ).first()
        
        if not favorito:
            return jsonify({'error': 'Favorito não encontrado'}), 404
        
        db.session.delete(favorito)
        db.session.commit()
        
        return jsonify({'message': 'Favorito removido com sucesso'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Rotas para páginas HTML

@app.route('/favoritos')
def favoritos():
    try:
        usuario_id = session.get('usuario_id')
        if not usuario_id:
            return redirect(url_for('login'))

        favoritos = Favorito.query.filter_by(usuario_id=usuario_id)\
                                  .order_by(Favorito.data_adicionado.desc()).all()

        favoritos_por_cidade = {}
        for favorito in favoritos:
            cidade = favorito.cidade.title()
            if cidade not in favoritos_por_cidade:
                favoritos_por_cidade[cidade] = {
                    'atividades': [],
                    'pontos_turisticos': []
                }

            if favorito.tipo == 'atividade':
                favoritos_por_cidade[cidade]['atividades'].append(favorito)
            else:
                favoritos_por_cidade[cidade]['pontos_turisticos'].append(favorito)

        return render_template(
            'global/favoritos.html',
            favoritos_por_cidade=favoritos_por_cidade,
            total_favoritos=len(favoritos)
        )

    except Exception as e:
        return render_template(
            'global/favoritos.html',
            favoritos_por_cidade={},
            total_favoritos=0,
            error='Erro ao carregar favoritos'
        )

@app.route('/favoritos/remover/<int:favorito_id>')
def remover_favorito_web(favorito_id):
    """Remove favorito via interface web"""
    try:
        usuario_id = session['usuario_id']
        favorito = Favorito.query.filter_by(
            id=favorito_id,
            usuario_id=usuario_id
        ).first()
        
        if favorito:
            db.session.delete(favorito)
            db.session.commit()
        
        return redirect(url_for('favoritos'))
    
    except Exception as e:
        return redirect(url_for('favoritos'))

# Função helper para verificar se um item é favorito
def is_favorito(usuario_id, item_id):
    """Verifica se um item é favorito do usuário"""
    return Favorito.query.filter_by(
        usuario_id=usuario_id,
        item_id=item_id
    ).first() is not None

# Template filter para usar no Jinja2
@app.template_filter('is_favorito')
def is_favorito_filter(item_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return False
    return is_favorito(usuario_id, item_id)


if __name__ == '__main__':
    app.run(debug=True)