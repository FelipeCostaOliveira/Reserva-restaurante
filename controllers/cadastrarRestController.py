from flask import Blueprint, session, flash, redirect, request
import mysql.connector
import createDataBase

cadastrarRestaurante_bp = Blueprint('cadastrar', __name__)

@cadastrarRestaurante_bp.route('/cadastrarRestaurante', methods=['POST'])
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