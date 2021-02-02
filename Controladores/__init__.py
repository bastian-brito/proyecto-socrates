from flask import Blueprint

#Aqui se crea el Blue Print de Usuario
usuarios_bp = Blueprint('usuarios', __name__, template_folder='templates')

from . import Usuarios_Controler