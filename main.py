from flask import Flask, render_template, request, flash, redirect, session
import json
import mysql.connector
import database

app = Flask(__name__)
app.secret_key = 'felipe'


# Criar Banco de Dados
DBhost = 'localhost' 
DBname = 'SistemaReservas'
DBuser = 'root'
DBpassword = ''


# CRIAR TABELA DE BANCO DE DADOS
connection = database.create_server_connection(DBhost, DBuser, DBpassword)     
query_database = f"create database {DBname}"
database.create_database(connection, query_database, DBname)
# Criar Tabela usuario
NameTabela = 'usuario'
query = f"""
CREATE TABLE {NameTabela} 
(id_usuario INT NOT NULL AUTO_INCREMENT,
email VARCHAR(45) NOT NULL,
senha VARCHAR(45) NOT NULL,
PRIMARY KEY (id_usuario)) 
DEFAULT CHARSET=utf8mb4;
"""
new_connection = database.create_new_server_connection(DBhost, DBuser, DBname, DBpassword)
database.create_table(new_connection, NameTabela, query)

# Criar tabela restaurante
NameTabela2 = 'restaurante'
query2 = f"""
CREATE TABLE {NameTabela2}
(id_restaurante INT NOT NULL AUTO_INCREMENT,
nome VARCHAR(45) NOT NULL,
dono VARCHAR(45) NOT NULL,
descricao VARCHAR(255) NOT NULL,
rua VARCHAR(100) NOT NULL,
bairro VARCHAR(100) NOT NULL,
numero INT NOT NULL,
mesasDisponiveis INT,
PRIMARY KEY(id_restaurante))
DEFAULT CHARSET=utf8mb4;
"""
new_connection2 = database.create_new_server_connection(DBhost, DBuser, DBname, DBpassword)
database.create_table(new_connection2, NameTabela2, query2)

# Criar tabela reserva
NameTabela3 = 'reserva'
query3 = f"""
CREATE TABLE {NameTabela3} 
(id_reserva INT NOT NULL AUTO_INCREMENT,
id_restaurante INT NOT NULL,
num_pessoas INT NOT NULL,
horario TIME NOT NULL,
data DATE NOT NULL,
FOREIGN KEY (id_restaurante) REFERENCES restaurante(id_restaurante) ON DELETE CASCADE,
PRIMARY KEY(id_reserva)) 
DEFAULT CHARSET=utf8mb4;
"""
new_connection3 = database.create_new_server_connection(DBhost, DBuser, DBname, DBpassword)
database.create_table(new_connection3, NameTabela3, query3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Equipe')
def equipe():
    return render_template('Equipe.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    flash('Você foi desconectado com sucesso.')
    return redirect('/login')

@app.route('/home')
def home():
    connectBD = mysql.connector.connect(
        host=DBhost,
        database=DBname,
        user=DBuser,
        password=DBpassword
    )
    
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        cursor.execute("SELECT id_restaurante, nome, descricao, dono FROM restaurante;")
        restaurantes = cursor.fetchall()
        cursor.close()
        connectBD.close()
        print(restaurantes)
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página.')
        return redirect('/login')
    return render_template('home.html', restaurantes=restaurantes)

@app.route('/modelos')
def modelos():
    return render_template('modelos.html')

@app.route('/requisitos')
def requisitos():
    return render_template('requisitos.html')

@app.route('/reserva', methods=["POST"])
def reserva():
    id_restaurante = request.form.get("detalhes")
    connectBD = mysql.connector.connect(
        host=DBhost,
        database=DBname,
        user=DBuser,
        password=DBpassword
    )
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        cursor.execute(f"SELECT * FROM restaurante WHERE id_restaurante ={id_restaurante}")
        restaurante = cursor.fetchone()
        cursor.close()
        connectBD.close()
        print(restaurante)
    
    return render_template('ReservaPage.html', restaurante=restaurante)

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
            usuarioId = usuario[0]
            usuarioEmail = usuario[1]
            usuarioSenha = usuario[2]
            contador += 1
            
            if usuarioEmail == email and usuarioSenha == senha:
                session['user_id'] = usuarioId
                session['user_email'] = email
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
        
        if len(usuariosBD) < 1:
                query = "insert into usuario values (default, %s, %s);"
                cursor.execute(query, dados)
                connectBD.commit()
                for usuario in usuariosBD:
                    session['user_id'] = usuario[0]
                    session['user_email'] = email
                return redirect('/home')
        else:
            for usuario in usuariosBD:
                contador += 1
                usuarioId = usuario[0]
                print(usuarioId)
                if usuario[1] == email:
                    flash('Usuário já cadastrado')
                    return redirect('/')
    
                if contador >= len(usuariosBD):
                    query = "insert into usuario values (default, %s, %s);"
                    cursor.execute(query, dados)
                    connectBD.commit()
                    session['user_id'] = usuarioId
                    session['user_email'] = email
                    return redirect('/home')

    if connectBD.is_connected():
        cursor.close()
        connectBD.close()

@app.route('/cadastrarRestaurante', methods=['POST'])
def cadastrarRestaurante():
    nome = request.form.get('nome')
    dono = request.form.get('dono')
    descricao = request.form.get('descricao')
    rua = request.form.get('rua')
    bairro = request.form.get('bairro')
    numero = request.form.get('numero')
    dados = nome, dono, descricao, rua, bairro, numero
    connectBD = mysql.connector.connect(
        host=DBhost,
        database=DBname,
        user=DBuser,
        password=DBpassword
    )
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        cursor.execute("SELECT * FROM restaurante WHERE nome = %s", (nome,))
        restaurantesBD = cursor.fetchone()
        if restaurantesBD:
            flash('Restaurante já cadastrado')
            return redirect('/')
        else:
            query = "INSERT INTO restaurante (nome, dono, descricao, rua, bairro, numero) VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute(query, dados)
            connectBD.commit()
            flash('Restaurante Cadastrado com sucesso. Faça login para fazer uma reserva')
            return redirect('/login')

    if connectBD.is_connected():
        cursor.close()
        connectBD.close()

@app.route('/cadastrarReserva', methods=['POST'])
def cadastrarReserva():
    restaurante_id = request.form.get('restaurante_id')
    data = request.form.get('data')
    hora = request.form.get('horario')
    hora = f'{hora}:00'
    numero_pessoas = request.form.get('num_pessoas')
    
    connectBD = mysql.connector.connect(
        host=DBhost,
        database=DBname,
        user=DBuser,
        password=DBpassword
    )
    
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        query = """
        INSERT INTO reserva (id_restaurante, data, horario, num_pessoas)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (restaurante_id, data, hora, numero_pessoas))
        connectBD.commit()
        flash('Reserva cadastrada com sucesso!')
        return redirect('/home')

    if connectBD.is_connected():
        cursor.close()
        connectBD.close()

@app.route('/formularioReserva', methods=["POST"])
def formularioReserva():
    connectBD = mysql.connector.connect(
        host=DBhost,
        database=DBname,
        user=DBuser,
        password=DBpassword
    )
    
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        cursor.execute("SELECT id_restaurante, nome FROM restaurante;")
        restaurantes = cursor.fetchall()
        cursor.close()
        connectBD.close()
        print(restaurantes)
        
    return render_template('RealizarReserva.html', restaurantes=restaurantes)

        
if __name__ in "__main__":
    app.run(debug=True, port=5001)