from flask import Flask, render_template, request, flash, redirect
import json
app = Flask(__name__)
app.secret_key = 'felipe'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Equipe')
def equipe():
    return render_template('Equipe.html')

@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/home', methods=["POST"])
def home():
    email = request.form.get("email")
    senha = request.form.get("senha")
    
    with open('users.json') as usersTemp:
        usuarios = json.load(usersTemp)
        contador = 0
        for usuario in usuarios:
            contador += 1
            
            if usuario['email'] == email and usuario['senha'] == senha:
                return render_template("home.html")
                    
            if contador >= len(usuarios):
                flash('Usuário Inválido')
                return redirect("/login")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    user = []
    email = request.form.get('email')
    senha = request.form.get('senha')   
    user = [
        {
            "email" : email,
            "senha" : senha,
            
        }
    ]
    with open('users.json') as usersTemp:
        usuarios = json.load(usersTemp)
    usuarioNovo = user + usuarios
    with open('users.json', 'w') as gravarTemp:
        json.dump(usuarioNovo, gravarTemp, indent=4)      
    return render_template('home.html')  
        
if __name__ in "__main__":
    app.run(debug=True)