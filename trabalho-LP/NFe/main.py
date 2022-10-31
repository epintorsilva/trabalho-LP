from tabnanny import check
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .pyauto import auto
''' 
Este arquivo guarda as funções mapeadas a rotas não relacionadas à operações de autenticação.
As rotas são configuradas com decoradores sobre a class Blueprint do flask. O módulo é
importado no arquivo __init__.py e registrado no app lá instanciado como um blueprint.
'''
main = Blueprint('main', __name__)

'''
    Função para a rota principal da aplicação, que retorna a página inicial.
'''
@main.route('/')
def index():
    return render_template('index.html')

'''
    Função para a rota de perfil.
'''
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


'''
    Função para a rota da página de edição de perfil.
'''
@main.route('/profile-edit')
@login_required
def profile_edit():
    return render_template('profile-edit.html', user=current_user)

'''
    Função para a rota de edição de perfil, que recebe os dados atualizados do usuário 
    (nome de usuário, cpf, cnpj e senha e substitui os antigos por eles no banco de dados.
'''
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

'''
    Função que retorna a página de edição de senha.
'''
@main.route('/change-password')
@login_required
def change_password():
    return render_template('change_password.html')

'''
    Função lida com a operação de edição de senha, recebendo a senha nova do usuário e a substi-
    tuindo no banco de dados.
'''
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

'''
    Função para a rota de emissão de notas, que retorna a página correspondente.
'''
@main.route('/emissao-nota')
@login_required
def emissao_nota():
    return render_template('emissao_nota.html')

'''
    Esta função se encarrega da automação da emissão das notas, acessando o site da prefeitura,
    preenchendo seus formulários e gerando as notas fiscais correspondentes.
'''
@main.route('/emissao_nota_post', methods=['POST'])
@login_required
def emissao_nota_post():
    arquivo = request.files.get("arquivo")
    auto(arquivo, session['senha'], current_user.cpf, current_user.cnpj)
    if not arquivo.filename:
        flash('Nenhum arquivo selecionado.')
        return redirect(url_for('main.emissao_nota'))

    return render_template("emissao_realizada.html")

