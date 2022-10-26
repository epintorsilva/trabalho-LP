from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    lembrar = True if request.form.get('lembrar') else False

    user = User.query.filter_by(usuario=usuario).first()

    if not user or not check_password_hash(user.senha, senha):
        flash('Usuário ou senha incorretos. Por favor cheque seus dados e tente novamente.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=lembrar)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    usuario = request.form.get('usuario')
    senha1 = request.form.get('senha1')
    senha2 = request.form.get('senha2')

    cpf = request.form.get('cpf')
    cnpj = request.form.get('cnpj')

    user = User.query.filter_by(usuario=usuario).first()

    if senha1 != senha2:
        flash('Senhas informadas são diferentes')
        return redirect(url_for('auth.signup'))

    if usuario == '' or senha1 == '' or senha2 == '':
        flash('Os campos de nome de usuário, senha e confirmação de senha são obrigatórios.')
        return redirect(url_for('auth.signup'))

    if user:
        flash('Nome de usuário já existe')
        return redirect(url_for('auth.signup'))
    
    new_user = User(usuario=usuario, senha=generate_password_hash(senha1, method='sha256'), cpf=cpf, cnpj=cnpj)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

