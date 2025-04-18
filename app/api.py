from flask import Flask, render_template, send_from_directory, redirect, url_for, request

app = Flask(__name__)

# Configuração das pastas de templates e arquivos estáticos
app.template_folder = 'templates'
app.static_folder = 'static'

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