from flask import Blueprint, flash, session, redirect, render_template
import mysql.connector
import createDataBase

editarRestaurante_bp = Blueprint('editar', __name__)

@editarRestaurante_bp.route('/editarRestaurante', methods=['GET'])
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
