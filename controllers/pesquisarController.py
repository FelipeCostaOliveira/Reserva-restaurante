from flask import Blueprint,request, render_template
import mysql.connector
import createDataBase

pesquisa_bp = Blueprint('pesquisa', __name__)

@pesquisa_bp.route('/pesquisar', methods=['GET'])
def pesquisa():
    restaurante_pesquisado = request.args.get('query')
    connectBD = mysql.connector.connect(
        host=createDataBase.DBhost,
        database=createDataBase.DBname,
        user=createDataBase.DBuser,
        password=createDataBase.DBpassword
    )
    restaurantes = []
    resultados_pesquisa = []

    if connectBD.is_connected():
        cursor = connectBD.cursor()

        # Buscar todos os restaurantes para as seções 'em alta' e 'disponíveis'
        cursor.execute("SELECT id_restaurante, nome, descricao, dono FROM restaurante;")
        restaurantes = cursor.fetchall()

        # Caso exista o termo de pesquisa, buscar apenas restaurantes que correspondem ao termo
        if restaurante_pesquisado:
            query = """
                SELECT id_restaurante, nome, descricao, dono
                FROM restaurante 
                WHERE nome LIKE %s OR descricao LIKE %s
            """
            termo_sql = f"%{restaurante_pesquisado}%"
            cursor.execute(query, (termo_sql, termo_sql))
            resultados_pesquisa = cursor.fetchall()

        cursor.close()
        connectBD.close()

    return render_template('cliente/home.html', restaurantes=restaurantes, resultados_pesquisa=resultados_pesquisa, query=restaurante_pesquisado)
