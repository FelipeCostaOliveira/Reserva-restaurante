from flask import Flask, render_template, request, flash, redirect
import json
import mysql.connector
import database

app = Flask(__name__)
app.secret_key = 'felipe'


# Criar Banco de Dados
DBname = 'usuarios'
connection = database.create_server_connection("localhost", "root", "root")     
query_database = f"create database {DBname}"
database.create_database(connection, query_database, DBname)
# Criar Tabela
# NameTabela = 'usuario'
new_connection = database.create_new_server_connection("localhost", "root", DBname, "root")
database.create_table(new_connection, 'usuario')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Equipe')
def equipe():
    return render_template('Equipe.html')

@app.route('/login')
def login():
    return render_template('login.html')


# Autenticar Usuário
@app.route('/home', methods=["POST"])
def home():
    email = request.form.get("email")
    senha = request.form.get("senha")
    connectBD = mysql.connector.connect(
        host='localhost',
        database='usuarios',
        user='root',
        password='root'
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
                return render_template("home.html")
                    
            if contador >= len(usuariosBD):
                flash('Usuário Inválido')
                return redirect("/login")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    user = []
    email = request.form.get('email')
    senha = request.form.get('senha')   
    connectBD = mysql.connector.connect(
        host='localhost',
        database='usuarios',
        user='root',
        password='root'
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
                    return render_template('home.html')

    if connectBD.is_connected():
        cursor.close()
        connectBD.close()
    
    # user = [
    #     {
    #         "email" : email,
    #         "senha" : senha,
            
    #     }
    # ]
    # with open('users.json') as usersTemp:
    #     usuarios = json.load(usersTemp)
    # usuarioNovo = user + usuarios
    # with open('users.json', 'w') as gravarTemp:
    #     json.dump(usuarioNovo, gravarTemp, indent=4)      
    # return render_template('home.html')  
        
if __name__ in "__main__":
    app.run(debug=True)