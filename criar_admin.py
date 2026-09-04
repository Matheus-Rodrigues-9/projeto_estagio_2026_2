from getpass import getpass

from werkzeug.security import generate_password_hash

from app import app, db, Admin


with app.app_context():

    db.create_all()

    usuario = input("Usuário do administrador: ").strip()

    admin_existente = Admin.query.filter_by(
        usuario=usuario
    ).first()

    if admin_existente:
        print("Já existe um administrador com esse usuário.")

    else:
        senha = getpass("Senha: ")
        confirmar_senha = getpass("Confirme a senha: ")

        if senha != confirmar_senha:
            print("As senhas não coincidem.")

        elif len(senha) < 6:
            print("A senha deve possuir pelo menos 6 caracteres.")

        else:
            novo_admin = Admin(
                usuario=usuario,
                senha_hash=generate_password_hash(senha)
            )

            db.session.add(novo_admin)
            db.session.commit()

            print("Administrador criado com sucesso!")