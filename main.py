from flask import Flask, render_template, request, flash, redirect
import json
import mysql.connector
import database

app = Flask(__name__)
app.secret_key = 'felipe'


# Criar Banco de Dados
DBhost = 'localhost' 
DBname = 'SistemaReservas'
DBuser = 'root'
DBpassword = 'root'


# CRIAR TABELA DE BANCO DE DADOS
connection = database.create_server_connection(DBhost, DBuser, DBpassword)     
query_database = f"create database {DBname}"
database.create_database(connection, query_database, DBname)
# Criar Tabela usuario
NameTabela = 'usuario'
query = f"CREATE TABLE {NameTabela} (id INT NOT NULL AUTO_INCREMENT, email VARCHAR(45) NOT NULL, senha VARCHAR(45) NOT NULL, PRIMARY KEY (id)) DEFAULT CHARSET=utf8mb4;"
new_connection = database.create_new_server_connection(DBhost, DBuser, DBname, DBpassword)
database.create_table(new_connection, NameTabela, query)

# Criar tabela restaurante
NameTabela2 = 'restaurante'
query2 = f"CREATE TABLE {NameTabela2} (id INT NOT NULL AUTO_INCREMENT, nome VARCHAR(45) NOT NULL, rua VARCHAR(100) NOT NULL, bairro VARCHAR(100) NOT NULL, numero INT NOT NULL,mesasDisponiveis INT, PRIMARY KEY(id)) DEFAULT CHARSET=utf8mb4;"
new_connection2 = database.create_new_server_connection(DBhost, DBuser, DBname, DBpassword)
database.create_table(new_connection2, NameTabela2, query2)

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

@app.route('/novidades')
def novidades():
    return render_template('novidades.html') 

@app.route('/cadastroRestaurante')
def cadastroRestaurante():
    return render_template('cadastroRestaurante.html')

# Autenticar Usuário
@app.route('/autenticarUsuario', methods=["POST"])
def autenticarUsuario():
    email = request.form.get("email")
    senha = request.form.get("senha")
    connectBD = mysql.connector.connect(
        host=DBhost,
        database= DBname,
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
    senha = request.form.get('senha')   
    connectBD = mysql.connector.connect(
        host=DBhost,
        database=DBname,
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
                return redirect('/home')
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

@app.route('/cadastrarRestaurante', methods=['POST'])
def cadastrarRestaurante():
    nome = request.form.get('nome')
    rua = request.form.get('rua')
    bairro = request.form.get('bairro')
    numero = request.form.get('numero')
    connectBD = mysql.connector.connect(
        host=DBhost,
        database=DBname,
        user=DBuser,
        password=DBpassword
    )
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        cursor.execute("SELECT * FROM restaurante WHERE nome = %s", (nome,))
        restauranteBD = cursor.fetchone()
        
        if restauranteBD:
            flash('Restaurante já cadastrado')
            return redirect('/')
        else:
            query = "INSERT INTO restaurante (nome, rua, bairro, numero) VALUES (%s, %s, %s, %s);"
            cursor.execute(query, (nome, rua, bairro, numero))
            connectBD.commit()
            return redirect('/home')

    if connectBD.is_connected():
        cursor.close()
        connectBD.close()
        
if __name__ in "__main__":
    app.run(debug=True, port=5001)