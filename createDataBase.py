import database
# Criar Banco de Dados
DBhost = 'localhost' 
DBname = 'SistemaReservas'
DBuser = 'root'
DBpassword = 'gotec'

def criarBD():
    # CRIAR TABELA DE BANCO DE DADOS
    connection = database.create_server_connection(DBhost, DBuser, DBpassword)
    query_database = f"create database {DBname}"
    database.create_database(connection, query_database, DBname)
    # Criar Tabela usuario cliente
    NameTabela = 'usuario_cliente'
    query = f"""
    CREATE TABLE {NameTabela} 
    (id_usuario_cliente INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(45) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_usuario_cliente)) 
    DEFAULT CHARSET=utf8mb4;
    """
    new_connection = database.create_new_server_connection(DBhost, DBuser, DBname, DBpassword)
    database.create_table(new_connection, NameTabela, query)

    # Criar Tabela usuario cliente
    NameTabela = 'usuario_restaurante'
    query = f"""
    CREATE TABLE {NameTabela} 
    (id_usuario_restaurante INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(45) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_usuario_restaurante)) 
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