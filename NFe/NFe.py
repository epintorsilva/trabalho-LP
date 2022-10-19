from flask import Flask, render_template, request
from funcoes import cadastrar, login

NFe = Flask(__name__)

@NFe.route("/")
def pagina_inicial():
    return render_template("inicio.html")

@NFe.route("/registro")
def registrar():
    return render_template("registro.html")

@NFe.route("/cadastro",  methods =["POST"])
def criar_cadastro():
    usuario = request.form["usuario"]
    senha = request.form["senha"]
    CPF = request.form["CPF"]
    CNPJ = request.form["CNPJ"]
    return cadastrar(usuario,senha,CPF,CNPJ)


@NFe.route("/login", methods =["POST"])
def logar():

    usuario = request.form["usuario"]
    senha = request.form["senha"]
    return login(usuario,senha)

NFe.run()