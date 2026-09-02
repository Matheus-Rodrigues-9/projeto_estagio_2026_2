from datetime import datetime

from flask import Flask, render_template,request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "vetagenda-chave-secreta"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vetagenda.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Atendimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome_tutor = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)

    nome_animal = db.Column(db.String(100),nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    porte = db.Column(db.String(30), nullable=False)

    servico = db.Column(db.String(80), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    horario = db.Column(db.String(10), nullable=False)

    observacoes = db.Column(db.Text)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pendente"
    )

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )




@app.route("/")
def home():
    return render_template("index.html")


@app.route("/agendar", methods=["POST"])
def agendar():
    nome_tutor = request.form["nome_tutor"]
    email = request.form["email"]
    telefone = request.form["telefone"]
    nome_animal = request.form["nome_animal"]
    especie = request.form["especie"]
    porte = request.form["porte"]
    servico = request.form["servico"]
    data = request.form["data"]
    horario = request.form["horario"]
    observacoes = request.form["observacoes"]

    novo_atendimento = Atendimento(
        nome_tutor=nome_tutor,
        email=email,
        telefone=telefone,
        nome_animal=nome_animal,
        especie=especie,
        porte=porte,
        servico=servico,
        data=data,
        horario=horario,
        observacoes=observacoes
    )

    db.session.add(novo_atendimento)
    db.session.commit()

    flash("Solicitação enviada com sucesso! A clínica analisará o horário solicitado.", "sucesso")
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
