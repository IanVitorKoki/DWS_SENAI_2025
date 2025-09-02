# -*- coding: utf-8 -*-

# Passo 1: Importações e Configuração
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime   # Import para a data de publicação

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Sua-Segurança-Mora-Aqui'

# 🔹 Corrigido: antes estava escrito SQLACHEMY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==============================
# MODELOS DO BANCO DE DADOS
# ==============================

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuário: {self.nome}>'


# 🔹 Novo modelo Post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_publicacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post: {self.titulo}>"


# ==============================
# ROTAS DA APLICAÇÃO
# ==============================

# Rota principal que exibe o formulário e a lista de usuários
@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

# Rota para adicionar usuário
@app.route('/adicionar', methods=['POST'])
def adicionar_usuario():
    nome = request.form['nome']
    email = request.form['email']
    
    novo_usuario = Usuario(nome=nome, email=email)
    db.session.add(novo_usuario)
    db.session.commit()
    
    return redirect(url_for('index'))

# 🔹 Nova rota para listar posts
@app.route('/posts')
def listar_posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)


# ==============================
# INICIALIZAÇÃO DO BANCO E SERVIDOR
# ==============================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # Cria as tabelas Usuario e Post, se não existirem
    
    # Inicia o servidor de desenvolvimento do Flask
    app.run(host='0.0.0.0', port=5001, debug=True)
