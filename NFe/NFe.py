from flask import Flask, render_template, request, session
from funcoes import cadastrar, login
import pandas as pd
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('static','uploads')
ALLOWED_EXTENSIONS = {'csv'}

NFe = Flask(__name__)
NFe.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
NFe.secret_key = 'Chave secreta para seção flask'

df = pd.read_csv('data/comment.csv')

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

@NFe.route("/csv-show-upload", methods=["GET"])
def csv_showUpload():
    return render_template("index-upload-and-show-data.html")

@NFe.route('/csv-carregado', methods=['POST','GET'])
def upload_arquivo():
    if request.method == 'POST':
        # upload file flask
        uploaded_df = request.files['arquivo-carregado']
 
        # Extracting uploaded data file name
        data_filename = secure_filename(uploaded_df.filename)
 
        # flask upload file to database (defined uploaded folder in static path)
        uploaded_df.save(os.path.join(NFe.config['UPLOAD_FOLDER'], data_filename))
 
        # Storing uploaded file path in flask session
        session['uploaded_data_file_path'] = os.path.join(NFe.config['UPLOAD_FOLDER'], data_filename)
 
        return render_template('index-upload-and-show-data-page2.html')
 

@NFe.route('/show-data',  methods=("POST", "GET"))
def show_data():
    # Retrieving uploaded file path from session
    data_file_path = session.get('uploaded_data_file_path', None)
 
    # read csv file in python flask (reading uploaded csv file from uploaded server location)
    uploaded_df = pd.read_csv(data_file_path)
 
    # pandas dataframe to html table flask
    uploaded_df_html = uploaded_df.to_html()
    return render_template('show-csv-data.html', data_var = uploaded_df_html)

NFe.run()

