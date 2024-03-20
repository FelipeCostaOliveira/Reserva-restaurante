from mysql.connector import Error
import pandas as pd
import mysql.connector

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query, DBName):
    cursor = connection.cursor()
    try:
        cursor.execute(f"SHOW DATABASES LIKE '{DBName}'")
        resultado = cursor.fetchone()
        if not resultado:
            cursor.execute(query)
            print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")
        


def create_new_server_connection(host_name, user_name, database_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            database=database_name,
            password=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_table(connection, NameTabela):
    cursor = connection.cursor()
    try:
        cursor.execute(f"SHOW TABLES LIKE '{NameTabela}'")
        resultado = cursor.fetchone()
        query = f"CREATE TABLE {NameTabela} (id INT NOT NULL AUTO_INCREMENT, email VARCHAR(45) NOT NULL, senha VARCHAR(45) NOT NULL, PRIMARY KEY (id)) DEFAULT CHARSET=utf8mb4;"
        if not resultado:
            cursor.execute(query)
            print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")
    

    
    