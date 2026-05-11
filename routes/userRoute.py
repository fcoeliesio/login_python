from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from controllers.user_controller import *

user_bp = Blueprint('user', __name__)

# HOME
@user_bp.route('/')
def index():
    return render_template('index.html')

# CADASTRO
@user_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        user, error = create_user_controller(request.form)

        if error == "USERNAME_EXISTS":
            flash("Usuário já existe!", "error")
            return render_template("login.html")

        flash("Usuário criado com sucesso!", "success")
        return render_template("login.html")

    return render_template("cadastro.html")


# LOGIN
@user_bp.route('/login', methods=['GET', 'POST'])
def login_user():

    if request.method == 'GET':
        return render_template('login.html')

    user, error = login_user_controller(request.form)

    if error:
        flash(error, "error")
        return render_template('login.html')

    session['username'] = user.username

    return redirect(url_for('user.usuario', username=user.username))


# PERFIL
@user_bp.route('/<username>')
def usuario(username):

    if 'username' not in session:
        return redirect(url_for('user.login_user'))

    user, error = get_user_controller(username)

    if error:
        return error, 404

    return render_template('usuario.html', user=user)


# LOGOUT
@user_bp.route('/logout', methods=['POST'])
def logout_user():

    session.clear()

    return redirect(url_for('user.index'))


# REDEFINIR SENHA
@user_bp.route('/redefinir-senha', methods=['POST'])
def redefine_password():

    return reset_password_controller()


# DELETAR USUÁRIO
@user_bp.route('/deletar', methods=['POST'])
def delete_user():

    result, status = delete_user_controller(session.get('username'))

    return result, status