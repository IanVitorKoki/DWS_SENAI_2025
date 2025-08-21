from datetime import date
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, ValidationError

# --- Configuração da Aplicação Flask ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-super-secreta'


class EventoForm(FlaskForm):
    nome_evento = StringField("Nome do Evento", validators=[DataRequired("Informe o nome do evento.")])
    data_evento = DateField("Data do Evento", format="%Y-%m-%d", validators=[DataRequired("Informe a data do evento.")])
    organizador = StringField("Organizador", validators=[DataRequired("Informe o nome do organizador.")])
    tipo_evento = SelectField("Tipo de Evento", choices=[("Palestra", "Palestra"), ("Workshop", "Workshop"), ("Meetup", "Meetup"), ("Outro", "Outro")])
    mensagem = TextAreaField("Descrição / Observações", validators=[Length(max=500, message="Máximo de 500 caracteres.")])
    enviar = SubmitField("Cadastrar Evento")

    # Validador: data do evento não pode ser no passado
    def validate_data_evento(self, field):
        if field.data < date.today():
            raise ValidationError("A data do evento não pode ser no passado.")

    # Validação condicional: se tipo 'Outro', descrição obrigatória
    def validate_mensagem(self, field):
        if self.tipo_evento.data == "Outro" and not (field.data or "").strip():
            raise ValidationError("Descrição é obrigatória para eventos do tipo 'Outro'.")

# --- Rotas da Aplicação ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/vazio", methods=["GET", "POST"])
def vazio():
    form = EventoForm()
    if form.validate_on_submit():
        flash(f"Evento '{form.nome_evento.data}' cadastrado com sucesso para {form.data_evento.data}!", "success")
        return render_template("sucesso.html", nome_usuario=form.organizador.data)
    return render_template("formulario.html", form=form, title="Formulário Vazio")

@app.route("/via-argumentos", methods=["GET", "POST"])
def via_argumentos():
    form = EventoForm(
        nome_evento="Encontro de Devs",
        organizador="Comunidade Python",
        tipo_evento="Meetup",
    )
    if form.validate_on_submit():
        flash("Dados atualizados e enviados com sucesso!", "success")
        return render_template("sucesso.html", nome_usuario=form.organizador.data)
    return render_template("formulario.html", form=form, title="Preenchido via Argumentos")

@app.route("/via-objeto", methods=["GET", "POST"])
def via_objeto():
    class EventoMock:
        def __init__(self, nome_evento, data_evento, organizador, tipo_evento, mensagem):
            self.nome_evento = nome_evento
            self.data_evento = data_evento
            self.organizador = organizador
            self.tipo_evento = tipo_evento
            self.mensagem = mensagem

    # Exemplo com dados do "banco"
    from datetime import date, timedelta
    obj = EventoMock(
        nome_evento="Workshop de Flask",
        data_evento=date.today() if date.today().weekday() != 6 else date.today(),
        organizador="SENAI",
        tipo_evento="Workshop",
        mensagem="Evento prático de Flask-WTF."
    )

    form = EventoForm(obj=obj)

    if form.validate_on_submit():
        flash("Dados atualizados e enviados com sucesso!", "success")
        return render_template("sucesso.html", nome_usuario=form.organizador.data)
    return render_template("formulario.html", form=form, title="Preenchido via Objeto")

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True)