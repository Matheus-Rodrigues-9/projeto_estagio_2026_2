from datetime import datetime

from flask import Flask, render_template,request, redirect, url_for, flash, session
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

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == "admin" and senha == "1234":
            session["admin_logado"] = True
            return redirect(url_for("admin"))

        flash("Usuário ou senha inválidos.", "erro")
    return render_template("login.html")    

@app.route("/admin")
def admin():

    if not session.get("admin_logado"):
        return redirect(url_for("login"))

    atendimentos = Atendimento.query.order_by(
        Atendimento.data.asc(),
        Atendimento.horario.asc()
    ).all()
    
    return render_template(
        "admin.html",
        atendimentos=atendimentos
    )

@app.route("/admin/atendimento/<int:id>/status", methods=["POST"])
def alterar_status(id):
    if not session.get("admin_logado"):
        return redirect(url_for("login"))
        
    atendimento = db.get_or_404(Atendimento, id)

    novo_status = request.form["status"]

    status_permitidos = ["pendente", "confirmado", "cancelado"]
    
    if novo_status not in status_permitidos:
        flash("Status inválido.", "erro")
        return redirect(url_for("admin"))

    if novo_status == "confirmado":

        conflito = Atendimento.query.filter_by(
            data=atendimento.data,
            horario=atendimento.horario,
            status="confirmado"
        ).filter(
            Atendimento.id != atendimento.id
        ).first()
        if conflito:
            flash(
                "Não foi possível confirmar: Já existe um atendimento confirmado nesse horário.", "erro"
            )
            
            return redirect(url_for("admin"))
    
    atendimento.status = novo_status

    db.session.commit()

    flash("Status atualizado com sucesso.", "sucesso")
    return redirect(url_for("admin"))

@app.route("/logout")
def logout():
    session.pop("admin_logado", None)

    flash("Logout realizado com sucesso.", "sucesso")
    
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
