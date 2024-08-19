from flask import Flask, render_template, request, flash, redirect
import json
import mysql.connector
import database

app = Flask(__name__)
app.secret_key = 'felipe'


# Criar Banco de Dados
DBhost = 'localhost' 
DBname = 'usuarios'
DBuser = 'root'
DBpassword = ''


# CRIAR TABELA DE BANCO DE DADOS
# connection = database.create_server_connection(DBhost, DBuser, DBpassword)     
# query_database = f"create database {DBname}"
# database.create_database(connection, query_database, DBname)
# Criar Tabela
# NameTabela = 'usuario'
# new_connection = database.create_new_server_connection(DBhost, DBuser, DBname, DBpassword)
# database.create_table(new_connection, 'usuario')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Equipe')
def equipe():
    return render_template('Equipe.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/modelos')
def modelos():
    return render_template('modelos.html')

@app.route('/requisitos')
def requisitos():
    return render_template('requisitos.html')

@app.route('/reserva')
def reserva():
    return render_template('ReservaPage.html')

@app.route('/RealizarReserva')
def realizar_reserva():
    return render_template('RealizarReserva.html')

# Autenticar Usuário
@app.route('/autenticarUsuario', methods=["POST"])
def autenticarUsuario():
    email = request.form.get("email")
    senha = request.form.get("senha")
    connectBD = mysql.connector.connect(
        host=DBhost,
        database='usuarios',
        user=DBuser,
        password=DBpassword
    )
    contador = 0
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        cursor.execute('select * from usuario;')
        usuariosBD = cursor.fetchall()
        for usuario in usuariosBD:
            usuarioEmail = usuario[1]
            usuarioSenha = usuario[2]
            contador += 1
            
            if usuarioEmail == email and usuarioSenha == senha:
                return redirect('/home')
                    
            if contador >= len(usuariosBD):
                flash('Usuário Inválido')
                return redirect("/login")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    user = []
    email = request.form.get('email')
    senha = request.form.get('password')   
    connectBD = mysql.connector.connect(
        host=DBhost,
        database='usuarios',
        user=DBuser,
        password=DBpassword
    )
    contador = 0
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        dados = email, senha
        cursor.execute("select * from usuario")
        usuariosBD = cursor.fetchall()
        
        if  len(usuariosBD) < 1:
                query = "insert into usuario values (default, %s, %s);"
                cursor.execute(query, dados)
                connectBD.commit()
                return render_template('home.html')
        else:
            for usuario in usuariosBD:
                contador += 1
                if usuario[1] == email:
                    flash('Usuário já cadastrado')
                    return redirect('/')
    
                if contador >= len(usuariosBD):
                    query = "insert into usuario values (default, %s, %s);"
                    cursor.execute(query, dados)
                    connectBD.commit()
                    return redirect('/home')

    if connectBD.is_connected():
        cursor.close()
        connectBD.close()

@app.route('/novidades')
def novidades():
    return render_template('novidades.html') 

        
if __name__ in "__main__":
    app.run(debug=True)