from flask import Flask, render_template, request, flash, redirect, session
from flask_bcrypt import generate_password_hash, check_password_hash
import mysql.connector
import createDataBase
import funcoes

app = Flask(__name__)
app.secret_key = 'felipe'

createDataBase.criarBD()

# LandingPage

@app.route('/')
def index():
    return render_template('landingPage/index.html')

@app.route('/Equipe')
def equipe():
    return render_template('landingPage/Equipe.html')

@app.route('/login')
def login():
    return render_template('landingPage/login.html')

@app.route('/loginDono')
def loginDono():
    return render_template('restaurante/LoginDono.html')

@app.route('/modelos')
def modelos():
    return render_template('landingPage/modelos.html')

@app.route('/requisitos')
def requisitos():
    return render_template('landingPage/requisitos.html')

@app.route('/cadastroRestaurante')
def cadastroRestaurante():
    return render_template('restaurante/CadastrarDono.html')

# Restaurantes

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
        host=createDataBase.DBhost,
        database=createDataBase.DBname,
        user=createDataBase.DBuser,
        password=createDataBase.DBpassword
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

@app.route('/editarRestaurante')
def editarRestaurante():
    return render_template('restaurante/EditarRestaurante.html')

# Clientes

@app.route('/novidades')
def novidades():
    return render_template('novidades.html')

@app.route('/home')
def home():
    connectBD = mysql.connector.connect(
        host=createDataBase.DBhost,
        database=createDataBase.DBname,
        user=createDataBase.DBuser,
        password=createDataBase.DBpassword
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
    return render_template('cliente/home.html', restaurantes=restaurantes)


    # Tela de detalhamento dos restaurantes

@app.route('/reserva', methods=["POST"])
def reserva():
    id_restaurante = request.form.get("detalhes")
    connectBD = mysql.connector.connect(
        host=createDataBase.DBhost,
        database=createDataBase.DBname,
        user=createDataBase.DBuser,
        password=createDataBase.DBpassword
    )
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        cursor.execute(f"SELECT * FROM restaurante WHERE id_restaurante ={id_restaurante}")
        restaurante = cursor.fetchone()
        cursor.close()
        connectBD.close()
        print(restaurante)
    
    return render_template('cliente/Detalhes.html', restaurante=restaurante)

    # Leva os dados do restaurante p/fazer a reserva
@app.route('/formularioReserva', methods=["POST"])
def formularioReserva():
    id_restaurante = request.form.get("reservar")
    connectBD = mysql.connector.connect(
        host=createDataBase.DBhost,
        database=createDataBase.DBname,
        user=createDataBase.DBuser,
        password=createDataBase.DBpassword
    )

    if connectBD.is_connected():
        cursor = connectBD.cursor()
        cursor.execute(f"SELECT id_restaurante, nome FROM restaurante where id_restaurante={id_restaurante};")
        restaurantes = cursor.fetchall()
        cursor.close()
        connectBD.close()

    return render_template('cliente/RealizarReserva.html', restaurantes=restaurantes)

    # Tela p/o clinte realizar a reserva

@app.route('/RealizarReserva')
def realizar_reserva():
    return render_template('RealizarReserva.html')

@app.route('/cadastrarReserva', methods=['POST'])
def cadastrarReserva():
    restaurante_id = request.form.get('restaurante_id')
    data = request.form.get('data')
    hora = request.form.get('horario')
    hora = f'{hora}:00'
    numero_pessoas = request.form.get('num_pessoas')
    print(restaurante_id)
    connectBD = mysql.connector.connect(
        host=createDataBase.DBhost,
        database=createDataBase.DBname,
        user=createDataBase.DBuser,
        password=createDataBase.DBpassword
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

# Autenticar Usuário
@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    funcoes.cadastrarUsuario("usuario_cliente")
    return redirect("/home")

@app.route('/autenticarUsuario', methods=["POST"])
def autenticarUsuario():
    funcoes.autenticarUsuario("usuario_cliente")
    return redirect("/home")

@app.route('/cadastrarGerente', methods=['POST'])
def cadastrarGerente():
    funcoes.cadastrarUsuario("usuario_restaurante")
    return redirect("/editarRestaurante")

@app.route('/autenticarGerente', methods=['POST'])
def autenticarGerente():
    funcoes.autenticarUsuario("usuario_restaurante")
    return redirect("/editarRestaurante")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    flash('Você foi desconectado com sucesso.')
    return redirect('/login')

if __name__ in "__main__":
    app.run(debug=True, port=5001)