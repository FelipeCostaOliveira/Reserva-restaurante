from flask import Blueprint, render_template

cadastro_bp = Blueprint('cadastro', __name__)

@cadastro_bp.route('/cadastroRestaurante')
def cadastroRestaurante():
    return render_template('restaurante/CadastrarDono.html')

