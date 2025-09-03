# -*- coding: utf-8 -*-
"""
Semana 6 - Exercício Prático: Minha Estante Virtual
Stack: Flask + Flask-SQLAlchemy + Flask-WTF + WTForms + wtforms-sqlalchemy
"""
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField

# -----------------------------------------------------------------------------
# Configuração da aplicação
# -----------------------------------------------------------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = "troque-esta-chave-para-uma-secreta"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///estante.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -----------------------------------------------------------------------------
# Modelos (Models)
# -----------------------------------------------------------------------------
class Autor(db.Model):
    __tablename__ = "autor"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)

    # Relacionamento 1:N (um Autor -> muitos Livros)
    livros = db.relationship("Livro", backref="autor", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Autor {self.nome!r}>"


class Livro(db.Model):
    __tablename__ = "livro"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)

    # Chave estrangeira referenciando Autor
    autor_id = db.Column(db.Integer, db.ForeignKey("autor.id"), nullable=False)

    def __repr__(self):
        return f"<Livro {self.titulo!r} ({self.ano_publicacao})>"


# -----------------------------------------------------------------------------
# Forms (Flask-WTF)
# -----------------------------------------------------------------------------
class AutorForm(FlaskForm):
    nome = StringField("Nome do Autor", validators=[DataRequired(), Length(min=2, max=120)])
    submit = SubmitField("Cadastrar Autor")


def autores_query():
    """Query usada pelo QuerySelectField para popular o dropdown de autores."""
    return Autor.query.order_by(Autor.nome)


class LivroForm(FlaskForm):
    titulo = StringField("Título do Livro", validators=[DataRequired(), Length(min=1, max=200)])
    ano_publicacao = IntegerField("Ano de Publicação", validators=[
        DataRequired(),
        NumberRange(min=1, max=9999, message="Ano deve estar entre 1 e 9999")
    ])
    autor = QuerySelectField(
        "Autor",
        query_factory=autores_query,
        allow_blank=False,
        get_label="nome"  # mostra o nome do autor no dropdown
    )
    submit = SubmitField("Cadastrar Livro")


# -----------------------------------------------------------------------------
# Rotas
# -----------------------------------------------------------------------------
@app.route("/autores", methods=["GET", "POST"])
def autores():
    form = AutorForm()
    if form.validate_on_submit():
        # Verifica se já existe um autor com esse nome
        nome = form.nome.data.strip()
        if Autor.query.filter_by(nome=nome).first():
            flash("Já existe um autor com esse nome.", "warning")
        else:
            db.session.add(Autor(nome=nome))
            db.session.commit()
            flash("Autor cadastrado com sucesso!", "success")
        return redirect(url_for("autores"))

    lista_autores = Autor.query.order_by(Autor.nome).all()
    return render_template("autores.html", form=form, autores=lista_autores)


@app.route("/", methods=["GET", "POST"])
@app.route("/livros", methods=["GET", "POST"])
def livros():
    form = LivroForm()
    if request.method == "POST":
        # Recarrega as opções do QuerySelectField antes de validar (boa prática)
        form.autor.query = autores_query()
    if form.validate_on_submit():
        livro = Livro(
            titulo=form.titulo.data.strip(),
            ano_publicacao=form.ano_publicacao.data,
            autor=form.autor.data  # já é o objeto Autor selecionado
        )
        db.session.add(livro)
        db.session.commit()
        flash("Livro cadastrado com sucesso!", "success")
        return redirect(url_for("livros"))

    lista_livros = Livro.query.order_by(Livro.titulo).all()
    return render_template("livros.html", form=form, livros=lista_livros)


# -----------------------------------------------------------------------------
# Inicialização do banco (apenas para desenvolvimento local)
# -----------------------------------------------------------------------------
@app.cli.command("init-db")
def init_db():
    """Comando Flask CLI para recriar o banco.
    Uso: flask --app app.py init-db
    """
    db.drop_all()
    db.create_all()
    print("Banco reiniciado com sucesso.")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001, debug=True)
