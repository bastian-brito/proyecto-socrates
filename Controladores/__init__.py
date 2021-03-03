from flask import Blueprint

#Aqui se crea el Blue Print de Usuario, Roles Aplicación
usuarios_bp = Blueprint('usuarios', __name__, template_folder='templates')
roles_aplicacion_bp = Blueprint('roles_aplicacion', __name__, template_folder='templates')
escuelas_bp = Blueprint('escuelas', __name__, template_folder='templates')

from . import Usuarios_Controler
from . import Roles_Aplicacion_Controller
from . import Escuela_Controller