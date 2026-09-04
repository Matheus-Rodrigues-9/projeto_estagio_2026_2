import os
from datetime import datetime, date

from flask import Flask, render_template,request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from dotenv import load_dotenv
from werkzeug.security import check_password_hash


load_dotenv()

app = Flask(__name__)

secret_key = os.getenv("SECRET_KEY")

if not secret_key:
    raise RuntimeError(
        "SECRET_KEY não configurada. Crie o arquivo .env com base no .env.example."
    )

app.secret_key = secret_key

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

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/agendar", methods=["POST"])
def agendar():

    nome_tutor = request.form.get("nome_tutor", "").strip()
    email = request.form.get("email", "").strip()
    telefone = request.form.get("telefone", "").strip()
    nome_animal = request.form.get("nome_animal", "").strip()
    especie = request.form.get("especie", "").strip()
    porte = request.form.get("porte", "").strip()
    servico = request.form.get("servico", "").strip()
    data_atendimento = request.form.get("data", "").strip()
    horario = request.form.get("horario", "").strip()
    observacoes = request.form.get("observacoes", "").strip()

    campos_obrigatorios = [
        nome_tutor,
        email,
        telefone,
        nome_animal,
        especie,
        porte,
        servico,
        data_atendimento,
        horario
    ]

    if not all(campos_obrigatorios):
        flash("Preencha todos os campos obrigatórios.", "erro")
        return redirect(url_for("home"))

    if "@" not in email or "." not in email:
        flash("Informe um email válido.", "erro")
        return redirect(url_for("home"))

    try:
        data_convertida = datetime.strptime(
            data_atendimento,
            "%Y-%m-%d"
        ).date()

    except ValueError:
        flash("Data de atendimento inválida.", "erro")
        return redirect(url_for("home"))
    
    if data_convertida < date.today():
        flash(
            "Não é possível solicitar atendimento para uma data passada.", "erro"
        )
        return redirect(url_for("home"))

    novo_atendimento = Atendimento(
        nome_tutor=nome_tutor,
        email=email,
        telefone=telefone,
        nome_animal=nome_animal,
        especie=especie,
        porte=porte,
        servico=servico,
        data=data_atendimento,
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

        admin = Admin.query.filter_by(
            usuario=usuario
        ).first()
        if admin and check_password_hash(admin.senha_hash, senha):

            session["admin_logado"] = True
            session["admin_id"] = admin.id

            return redirect(url_for("admin"))

        flash("Usuário ou senha inválidos.", "erro")

    return render_template("login.html")
    

@app.route("/admin")
def admin():

    if not session.get("admin_logado"):
        return redirect(url_for("login"))
    
    status_filtro = request.args.get("status", "")
    busca = request.args.get("busca", "").strip()

    consulta = Atendimento.query

    if status_filtro in ["pendente", "confirmado", "cancelado"]:
        consulta = consulta.filter_by(status=status_filtro)

    if busca:
        termo = f"%{busca}%"

        consulta = consulta.filter(
            or_(
                Atendimento.nome_tutor.ilike(termo),
                Atendimento.nome_animal.ilike(termo)
            )
        )

    atendimentos = consulta.order_by(
        Atendimento.data.asc(),
        Atendimento.horario.asc()
    ).all()

    total = Atendimento.query.count()

    pendentes = Atendimento.query.filter_by(
        status="pendente"
    ).count()

    confirmados = Atendimento.query.filter_by(
        status="confirmado"
    ).count()

    cancelados = Atendimento.query.filter_by(
        status="cancelado"
    ).count()

    return render_template(
        "admin.html",
        atendimentos=atendimentos,
        total=total,
        pendentes=pendentes,
        confirmados=confirmados,
        cancelados=cancelados,
        status_filtro=status_filtro,
        busca=busca
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
