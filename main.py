from flask import Flask, render_template, request, flash, redirect, session
import mysql.connector
import createDataBase
import funcoes
from views.landingRoutes import *
from views.cadastroRoutes import *
from views.registrarRestController import *
from controllers.pesquisarController import *
from controllers.cadastrarRestController import *
from controllers.editarRest import *
from controllers.atualizarRest import *

app = Flask(__name__)
app.secret_key = 'felipe'
createDataBase.criarBD()
# LandingPage
app.register_blueprint(landing_bp)

# cadastro do gerente
app.register_blueprint(cadastro_bp)

# Barra de pesquisa
app.register_blueprint(pesquisa_bp)

#cadastrar restaurante
    #front
app.register_blueprint(registrarRestaurante_bp)
    #back
app.register_blueprint(cadastrarRestaurante_bp)

#editar restaurante
app.register_blueprint(editarRestaurante_bp)
    
#atualizar restaurante
app.register_blueprint(atualizarRestaurante_bp)

# Clientes

@app.route('/novidades')
def novidades():
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
    return render_template('cliente/novidades.html', restaurantes=restaurantes)

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

@app.route('/reserva', methods=["GET","POST"])
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
    return redirect("/registrarRestaurante")

@app.route('/autenticarGerente', methods=['POST'])
def autenticarGerente():
    funcoes.autenticarUsuario("usuario_restaurante")
    return redirect("/registrarRestaurante")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    flash('Você foi desconectado com sucesso.')
    return redirect('/login')

@app.route('/voltar', methods=['POST'])
def voltar():
    referer = request.headers.get('Referer')
    if referer:
        return redirect(referer)

    return redirect('/')
if __name__ in "__main__":
    app.run(debug=True, port=5001)