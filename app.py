from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from formulario import IngresaUsuario
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_user import UserManager

# class ConfigClass(object):
#     """ Flask application config """

#     # Flask settings
#     SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

#     # Flask-SQLAlchemy settings
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///basic_app.sqlite'    # File-based SQL database
#     SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

#     # Flask-Mail SMTP server settings
#     MAIL_SERVER = 'smtp.gmail.com'
#     MAIL_PORT = 465
#     MAIL_USE_SSL = True
#     MAIL_USE_TLS = False
#     MAIL_USERNAME = 'email@example.com'
#     MAIL_PASSWORD = 'password'
#     MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'

#     # Flask-User settings
#     USER_APP_NAME = "Flask-User Basic App"      # Shown in and email templates and page footers
#     USER_ENABLE_EMAIL = True        # Enable email authentication
#     USER_ENABLE_USERNAME = False    # Disable username authentication
#     USER_EMAIL_SENDER_NAME = USER_APP_NAME
#     USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
#     USER_ENABLE_CONFIRM_EMAIL =False
#     USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = False
#     USER_LOGIN_TEMPLATE = 'flask_user/login.html'
#     USER_UNAUTHENTICATED_ENDPOINT = 'usuarios.login'



app = Flask(__name__)
#app.config.from_object(__name__+'.ConfigClass')
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
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


@app.route("/")
def inicio():    
    return render_template("Index.html")

# @app.route("/lista_roles")
# def lista_roles():
#     roles_aplicacion = Rol_Aplicacion.query.order_by(Rol_Aplicacion.fecha_creacion.asc()).all() 
#     return render_template("lista_roles.html", roles_aplicacion=roles_aplicacion)

@app.route("/nuevo_usuario_wtform", methods = ['GET', 'POST'])
def registrar_usuario():
    form = IngresaUsuario(request.form)
    if request.method ==  'POST' and form.validate():
        usuario =   Usuario(
                    name = form.nombres.data,
                    #fk_rol  =  1,
                    apellido_paterno =  form.apellido_paterno.data,
                    apellido_materno =  form.apellido_materno.data,
                    email =  form.correo.data,
                    password =  form.contraseña.data,
                    telefono =  form.telefono.data,
                    estado =  True)
        usuario.roles.append(Role(name='Admin', descripcion='Es Admin' , estado=True))
        usuario.set_password(password)
        usuario.save()
        # Dejamos al usuario logueado
        login_user(usuario, remember=True)        
        flash('Registro completo')
        return redirect("/")
    return render_template('nuevo_usuario_wtform.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))
 
if __name__ == "__main__":    
    app.run(debug=True)