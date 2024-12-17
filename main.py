from flask import Flask, render_template, request, flash, redirect, session
import mysql.connector
import createDataBase
import funcoes
from views.landingRoutes import *
from views.cadastroRoutes import *
from controllers.pesquisarController import *

app = Flask(__name__)
app.secret_key = 'felipe'
createDataBase.criarBD()
# LandingPage

app.register_blueprint(landing_bp)
app.register_blueprint(cadastro_bp)

# Barra de pesquisa
app.register_blueprint(pesquisar_bp)

# Restaurantes

@app.route('/registrarRestaurante')
def registrarRestaurante():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página.')
        return redirect('/loginDono')
    return render_template('restaurante/RegistrarRestaurante.html')

@app.route('/cadastrarRestaurante', methods=['POST'])
def cadastrarRestaurante():
    nome = request.form.get('nome')
    dono = request.form.get('dono')
    descricao = request.form.get('descricao')
    rua = request.form.get('rua')
    bairro = request.form.get('bairro')
    numero = request.form.get('numero')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    id_usuario_restaurante = session['user_id']
    print(id_usuario_restaurante)
    dados = nome, dono, descricao, rua, bairro, numero, email, telefone, id_usuario_restaurante
    connectBD = mysql.connector.connect(
        host=createDataBase.DBhost,
        database=createDataBase.DBname,
        user=createDataBase.DBuser,
        password=createDataBase.DBpassword
    )
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página.')
        return redirect('/login')
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        cursor.execute("SELECT * FROM restaurante WHERE nome = %s", (nome,))
        restaurante = cursor.fetchone()
        if restaurante:
            flash('Restaurante já cadastrado')
            return redirect('/registrarRestaurante')
        else:
            query = "INSERT INTO restaurante (nome, dono, descricao, rua, bairro, numero, email, telefone, id_usuario_restaurante) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(query, dados)
            connectBD.commit()
            return redirect('/editarRestaurante')

    if connectBD.is_connected():
        cursor.close()
        connectBD.close()

@app.route('/editarRestaurante')
def editarRestaurante():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página.')
        return redirect('/loginDono')
    dono_id = session['user_id']
    connectBD = mysql.connector.connect(
        host=createDataBase.DBhost,
        database=createDataBase.DBname,
        user=createDataBase.DBuser,
        password=createDataBase.DBpassword
    )
    
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        query = "SELECT * FROM restaurante WHERE id_usuario_restaurante = %s"
        cursor.execute(query, (dono_id,))
        restaurante = cursor.fetchone()
        cursor.close()
        connectBD.close
    if restaurante:
        return render_template('restaurante/EditarRestaurante.html', restaurante=restaurante)
    else: 
        flash('Nenhum restaurante encontrado para este dono.')
        return redirect('/loginDono')
    
@app.route('/atualizarRestaurante', methods=['POST'])
def atualizarRestaurante():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página.')
        return redirect('/loginDono')
    dono_id = session['user_id']
    nome = request.form.get('nome')
    dono = request.form.get('dono')
    descricao = request.form.get('descricao')
    rua = request.form.get('rua')
    bairro = request.form.get('bairro')
    numero = request.form.get('numero')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    connectBD = mysql.connector.connect(
        host=createDataBase.DBhost,
        database=createDataBase.DBname,
        user=createDataBase.DBuser,
        password=createDataBase.DBpassword
    )
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        query = """
            UPDATE restaurante
            SET nome = %s,dono = %s, descricao = %s, rua = %s, bairro = %s, numero = %s, email = %s, telefone = %s WHERE id_usuario_restaurante = %s
        """
        cursor.execute(query,(nome, dono, descricao, rua, bairro, numero, email, telefone, dono_id))
        connectBD.commit()
        cursor.close()
        connectBD.close() 
        flash("Restaurante atualizado")
        return redirect('/editarRestaurante')
    
@app.route('/deletarRestaurante', methods=['GET'])
def deletarRestaurante():
    restaurante_id = request.args.get('restaurante_id')
    connectBD = mysql.connector.connect(
        host=createDataBase.DBhost,
        database=createDataBase.DBname,
        user=createDataBase.DBuser,
        password=createDataBase.DBpassword
    )

    if connectBD.is_connected():
        cursor = connectBD.cursor()
        cursor.execute("DELETE FROM restaurante WHERE id_restaurante = %s", (restaurante_id,))
        connectBD.commit()
        cursor.close()
        connectBD.close()
        
        flash('Restaurante deletado com sucesso!')
        return redirect('/loginDono')

    flash('Erro ao conectar ao banco de dados.')
    return redirect('/home')
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