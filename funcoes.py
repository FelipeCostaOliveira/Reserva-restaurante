from flask import Flask, render_template, request, flash, redirect, session
from flask_bcrypt import generate_password_hash, check_password_hash
import mysql.connector
import createDataBase

def cadastrarUsuario(nomeTabela):
    email = request.form.get('email')
    senhaHash = generate_password_hash(request.form.get('senha')).decode('utf-8')  
    print(senhaHash)
    senha =  senhaHash
    connectBD = mysql.connector.connect(
        host=createDataBase.DBhost,
        database=createDataBase.DBname,
        user=createDataBase.DBuser,
        password=createDataBase.DBpassword
    )
    contador = 0
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        dados = email, senha
        cursor.execute(f"select * from {nomeTabela}")
        usuariosBD = cursor.fetchall()
        
        if len(usuariosBD) < 1:
                query = f"insert into {nomeTabela} values (default, %s, %s);"
                cursor.execute(query, dados)
                connectBD.commit()
                
        else:
            for usuario in usuariosBD:
                contador += 1
                
                if usuario[1] == email:
                    flash('Usuário já cadastrado')
                    return redirect('/')
    
                if contador >= len(usuariosBD):
                    query = f"insert into {nomeTabela} values (default, %s, %s);"
                    cursor.execute(query, dados)
                    connectBD.commit()
                
        cursor.execute(f"select * from {nomeTabela}")
        usuariosBD = cursor.fetchall()
        for usuario in usuariosBD:
            session['user_id'] = usuario[0]
            session['user_email'] = email       
           

    if connectBD.is_connected():
        cursor.close()
        connectBD.close()

def autenticarUsuario(nomeTabela):
    email = request.form.get("email")
    senha = request.form.get("senha")
    connectBD = mysql.connector.connect(
        host=createDataBase.DBhost,
        database= createDataBase.DBname,
        user=createDataBase.DBuser,
        password=createDataBase.DBpassword
    )
    contador = 0
    if connectBD.is_connected():
        cursor = connectBD.cursor()
        cursor.execute(f'select * from {nomeTabela};')
        usuariosBD = cursor.fetchall()
        for usuario in usuariosBD:
            usuarioId = usuario[0]
            usuarioEmail = usuario[1]
            usuarioSenha = usuario[2]
            contador += 1
            
            if usuarioEmail == email and check_password_hash(usuarioSenha, senha):
                session['user_id'] = usuarioId
                session['user_email'] = usuarioEmail
                return redirect('/home')
                    
            if contador >= len(usuariosBD):
                flash('Usuário Inválido')
                return redirect("/login")