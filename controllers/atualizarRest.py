from flask import Blueprint, session, flash, redirect, request
import mysql.connector
import createDataBase

atualizarRestaurante_bp = Blueprint('atualizar', __name__)

@atualizarRestaurante_bp.route('/atualizarRestaurante', methods=['POST'])
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
