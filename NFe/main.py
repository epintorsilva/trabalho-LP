from tabnanny import check
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
import time
import pandas as pd

from .teste import auto

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/profile-edit')
@login_required
def profile_edit():
    return render_template('profile-edit.html', user=current_user)

@main.route('/profile-edit', methods=['POST'])
@login_required
def profile_edit_post():
    usuario = request.form.get('usuario')

    cpf = request.form.get('cpf')
    cnpj = request.form.get('cnpj')

    user = User.query.filter_by(usuario=usuario).first()

    if user and user.usuario != current_user.usuario:
        flash('Nome de usuário já existe')
        return redirect(url_for('main.profile'))
    
    user = User.query.filter_by(usuario=current_user.usuario).first()

    user.usuario = usuario
    user.cpf=cpf
    user.cnpj=cnpj
    db.session.commit()
    flash('Dados atualizados com sucesso!')
    return redirect(url_for('main.profile'))

@main.route('/change-password')
@login_required
def change_password():
    return render_template('change_password.html')

@main.route('/change-password', methods=['POST'])
@login_required
def change_password_post():
    senha_atual = request.form.get('senha_atual')
    nova_senha_1 = request.form.get('nova_senha_1')
    nova_senha_2 = request.form.get('nova_senha_2')

    print(senha_atual)
    print(nova_senha_1)
    print(nova_senha_2)

    if(nova_senha_1 != nova_senha_2):
        flash('Novas enhas informadas são não iguais.')
        return redirect(url_for('main.change_password'))

    if not check_password_hash(current_user.senha, senha_atual):
        flash('Senha atual informada está incorreta.')
        return redirect(url_for('main.change_password'))

    user = User.query.filter_by(usuario=current_user.usuario).first()
    user.senha = generate_password_hash(nova_senha_1, method='sha256')
    print(user.senha)
    db.session.commit()
    current_user.senha = senha_atual
    flash('Senha trocada com sucesso!')
    return redirect(url_for('auth.logout'))

@main.route('/emissao-nota')
@login_required
def emissao_nota():
    return render_template('emissao_nota.html')

@main.route('/emissao_nota_post', methods=['POST'])
@login_required
def emissao_nota_post():
    arquivo = request.files.get("arquivo")
    auto(arquivo, session['senha'], current_user.cpf, current_user.cnpj)
    if not arquivo.filename:
        flash('Nenhum arquivo selecionado.')
        return redirect(url_for('main.emissao_nota'))

    return render_template("emissao_realizada.html")

