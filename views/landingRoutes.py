from flask import Blueprint, render_template

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/')
def index():
    return render_template('landingPage/index.html')

@landing_bp.route('/Equipe')
def equipe():
    return render_template('landingPage/Equipe.html')

@landing_bp.route('/login')
def login():
    return render_template('landingPage/login.html')

@landing_bp.route('/loginDono')
def loginDono():
    return render_template('restaurante/LoginDono.html')

@landing_bp.route('/modelos')
def modelos():
    return render_template('landingPage/modelos.html')


