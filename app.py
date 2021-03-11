from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
#from formulario import IngresaUsuario
from flask_migrate import Migrate
from flask_login import LoginManager, login_user
#from flask_wtf import CsrfProtect
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
#app.config.from_object(__name__+'.ConfigClass')
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
#Protección de ataque csrf
csrf = CSRFProtect(app)
app.config['SERVER_NAME']='sitio.tld:5000'
#app.url_map.default_subdomain = "www"

login_manager = LoginManager(app)
login_manager.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:@localhost/flask'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
from Modelo.Modelos import *
migrate = Migrate(app, db)
#user_manager = UserManager(app, db, User)
#Manejo de Migraciones de Base de Datos

#Aqui se importa la referencia Blue print de Usuarios
from Controladores.Usuarios_Controler import usuarios_bp
app.register_blueprint(usuarios_bp)

#Aqui se importa la referencia Blue print de Roles de Aplicación
from Controladores.Roles_Aplicacion_Controller import roles_aplicacion_bp
app.register_blueprint(roles_aplicacion_bp)

from Controladores.Escuela_Controller import escuelas_bp
app.register_blueprint(escuelas_bp)

#website_url = 'vibhu.gfg:5000'
#app.config['SERVER_NAME'] = website_url

@app.route("/")
def inicio():    
    return render_template("Index.html")

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))
 
if __name__ == "__main__":
    #website_url = '127.0.0.1 localhost.dev:5000'    
    #app.config['SERVER_NAME'] = website_url
    #app.url_map.default_subdomain = "www"
    #website_url = 'vibhu.gfg:5000'
    #app.config['SERVER_NAME'] = website_url
    # app.run(host='127.0.0.1', port=5000, debug=True)
    
    app.run(debug=True)