import sqlite3
from flask import render_template

def cadastrar(usuario,senha,CPF,CNPJ):

    conn = sqlite3.connect('NFe.db') 
    c = conn.cursor()
    j = c.execute(f"SELECT * FROM usuarios where usuario = '{usuario}'").fetchall()

    conn.commit()

    if j == []:
        c.execute(f"INSERT INTO usuarios VALUES ('{usuario}','{senha}','{CPF}','{CNPJ}')")
        conn.commit()
        return render_template("inicio.html")
    else: 
        return render_template("registro.html", erro = "usuario ja existente")
            

def login(usuario,senha):

    conn = sqlite3.connect('NFe.db') 
    c = conn.cursor()
    j = c.execute(f"SELECT * FROM usuarios where usuario = '{usuario}' and senha = '{senha}'").fetchall()
                         
    conn.commit()
    
    if j:
        return render_template("algumacoisa.html")
    else:
        return render_template("inicio", erro="Login Incorreto")
