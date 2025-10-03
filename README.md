# Rotas Nordestinas

Sistema web para divulgação e compartilhamento de rotas turísticas do Nordeste brasileiro, desenvolvido com Flask e SQLite.

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
- [Rotas Principais](#rotas-principais)
- [Licença](#licença)

## Sobre o Projeto

Rotas Nordestinas é uma plataforma web interativa que permite aos usuários:
- Explorar destinos turísticos do Nordeste
- Compartilhar feedbacks sobre cidades
- Sugerir novas rotas turísticas
- Favoritar atividades e pontos turísticos
- Sistema de moderação com denúncias e strikes

## Funcionalidades

### Para Usuários
- **Autenticação**: Sistema completo de cadastro e login
- **Exploração**: Navegue por cidades e estados do Nordeste
- **Feedbacks**: Compartilhe experiências sobre destinos visitados
- **Sugestões de Rotas**: Sugira novos destinos com fotos e pontos turísticos
- **Favoritos**: Salve seus lugares preferidos
- **Perfil**: Gerencie suas informações e sugestões

### Para Administradores
- **Moderação**: Analise feedbacks denunciados
- **Gestão de Sugestões**: Aprove ou rejeite sugestões de rotas
- **Sistema de Strikes**: Aplique penalidades a usuários infratores
- **Banimento**: Gerencie usuários banidos

## Tecnologias Utilizadas

- **Backend**: Flask 2.x
- **Banco de Dados**: SQLite com SQLAlchemy
- **Autenticação**: Werkzeug (hash de senhas)
- **Frontend**: HTML5, CSS3, JavaScript
- **Upload de Arquivos**: Werkzeug SecureFilename

## Estrutura do Projeto

```
Rotas_Nordestinas-main/
│
├── app/
│   ├── __pycache__/
│   ├── static/
│   │   ├── images/
│   │   ├── js/
│   │   ├── styles/
│   │   └── uploads/          # Fotos de sugestões
│   ├── templates/
│   │   ├── estados/          # Templates por estado
│   │   ├── global/           # Templates globais
│   │   ├── modais/           # Modais reutilizáveis
│   │   ├── base.html
│   │   ├── index.html
│   │   └── main.html
│   ├── app.py                # Aplicação principal
│   └── models.py             # Modelos do banco de dados
│
├── instance/
│   └── usuarios.db           # Banco de dados SQLite (criado automaticamente)
│
└── requeriments.txt          # Dependências do projeto
```

## Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone ou baixe o repositório:
```bash
cd Rotas_Nordestinas-main
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

3. Ative o ambiente virtual:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install Flask flask-sqlalchemy werkzeug
```

## Uso

1. Execute a aplicação:
```bash
python app/app.py
```

2. Acesse no navegador:
```
http://127.0.0.1:5000
```

3. **Primeiro Acesso**:
   - Cadastre-se na plataforma
   - Faça login com suas credenciais
   - Explore as cidades disponíveis

4. **Criar Conta Admin** (via console Python):
```python
from app.app import app, db
from app.models import Usuario

with app.app_context():
    admin = Usuario(
        nome='Admin',
        sobrenome='Sistema',
        email='admin@rotas.com',
        telefone='00000000000',
        usuario='admin',
        role='admin'
    )
    admin.set_senha('senha_admin')
    db.session.add(admin)
    db.session.commit()
```

## Estrutura do Banco de Dados

### Tabelas Principais

#### **usuarios**
- Cadastro de usuários
- Sistema de strikes e banimento
- Roles (user/admin)

#### **feedbacks**
- Avaliações de cidades
- Associados a usuários
- Sistema de denúncias

#### **sugestoes**
- Sugestões de novas rotas
- Status: pendente, aprovada, rejeitada
- Relacionamento com pontos turísticos e fotos

#### **favoritos**
- Itens favoritos dos usuários
- Suporta atividades e pontos turísticos

#### **denuncias**
- Sistema de moderação
- Relaciona usuários e feedbacks

## Rotas Principais

### Públicas
- `/` - Página inicial
- `/login` - Login de usuários
- `/cadastro` - Registro de novos usuários
- `/cidade/<nome_cidade>` - Página da cidade

### Autenticadas
- `/main` - Dashboard principal
- `/perfil` - Perfil do usuário
- `/sugerir_rota` - Formulário de sugestão
- `/favoritos` - Lista de favoritos

### Administrativas
- `/aprovar_sugestao/<id>` - Aprovar sugestão
- `/rejeitar_sugestao/<id>` - Rejeitar sugestão
- `/dar_strike/<usuario_id>/<feedback_id>` - Aplicar strike
- `/desbanir_usuario/<id>` - Remover banimento

### API
- `GET /api/favoritos` - Listar favoritos
- `POST /api/favoritos` - Adicionar favorito
- `DELETE /api/favoritos/<item_id>` - Remover favorito
- `GET /api/sugestao/<id>` - Detalhes da sugestão

## Configurações de Segurança

**IMPORTANTE**: Antes de usar em produção, altere as seguintes configurações em [app/app.py](app/app.py):

```python
# Altere a secret_key para uma chave aleatória forte
app.secret_key = 'sua_chave_secreta_super_segura_aqui'

# Configure banco de dados mais robusto se necessário
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
```

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Enviar pull requests

## Licença

Este projeto é de código aberto e está disponível para uso educacional e pessoal.

---

**Desenvolvido com ❤️ para promover o turismo no Nordeste brasileiro**
