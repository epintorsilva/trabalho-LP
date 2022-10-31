from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
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
    session["senha"] = senha
    return redirect(url_for('main.profile'))

@auth.route('/signup1')
def signup1():
    return render_template('signup1.html')

@auth.route('/signup2', methods=['POST'])
def signup2():
    usuario = request.form.get('usuario')
    senha1 = request.form.get('senha1')
    senha2 = request.form.get('senha2')

    if senha1 != senha2:
        flash('Senhas informadas são diferentes')
        return redirect(url_for('auth.signup1'))
    
    if usuario == '' or senha1 == '' or senha2 == '':
        flash('Os campos de nome de usuário, senha e confirmação de senha são obrigatórios.')
        return redirect(url_for('auth.signup1'))

    user = User.query.filter_by(usuario=usuario).first()
    if user:
        flash('Nome de usuário já existe. Vá para a página de login.')
        return redirect(url_for('auth.signup1'))

    args= {'usuario':usuario,'senha1':senha1,'senha2':senha2}
    
    return render_template('signup2.html', args=args)

@auth.route('/signup2_post', methods=['POST'])
def signup2_post():
    usuario = request.form.get('usuario')
    senha1 = request.form.get('senha1')
    senha2 = request.form.get('senha2')

    cpf = request.form.get('cpf')
    cnpj = request.form.get('cnpj')
    
    new_user = User(usuario=usuario, senha=generate_password_hash(senha1, method='sha256'), cpf=cpf, cnpj=cnpj)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

