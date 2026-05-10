from models.User import db, User
from werkzeug.security import generate_password_hash, check_password_hash


# CADASTRO
def create_user_controller(form):

    username = form.get('username')
    nome = form.get('nome')
    email = form.get('email')
    password = form.get('password')

    if User.query.filter_by(username=username).first():
        return None, "Usuário já existe!"

    hashed_password = generate_password_hash(password)

    new_user = User(
        username=username,
        nome=nome,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return new_user, None


# LOGIN
def login_user_controller(form):

    username = form.get('username')
    password = form.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        return user, None
    
    return None, "Credenciais inválidas!"

# PERFIL
def get_user_controller(username):

    user = User.query.filter_by(username=username).first()

    if not user:
        return None, "Usuário não encontrado!"

    return user, None


# DELETE (opcional futuro)
def delete_user_controller(username):
    
    user = User.query.filter_by(username=username).first()

    if not user:
        return "Usuário não encontrado!", 404

    
    db.session.delete(user)
    db.session.commit()

    return "Usuário deletado!", 200


# REDEFINIR SENHA (placeholder)
def reset_password_controller():
    return "Senha redefinida"