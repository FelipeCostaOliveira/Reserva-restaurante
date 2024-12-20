from flask import Blueprint, session, flash, redirect, request
import mysql.connector
import createDataBase

deletarRestaurante_bp = Blueprint('deletar', __name__)

@deletarRestaurante_bp.route('/deletarRestaurante', methods=['POST'])
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