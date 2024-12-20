from flask import Blueprint, flash, session, redirect, render_template

registrarRestaurante_bp = Blueprint('registrar', __name__)

@registrarRestaurante_bp.route('/registrarRestaurante', methods=['GET'])
def registrarRestaurante():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página.')
        return redirect('/loginDono')
    return render_template('restaurante/RegistrarRestaurante.html')
