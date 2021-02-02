from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from Modelo.Modelos import *
from formulario import IngresaUsuario
from flask_migrate import Migrate

app = Flask(__name__)

# Esta X eliminarse esta linea , no hay manejo de sesiones aun
app.secret_key = "Secret Key"

#Esta por dejar de existir en esta script -> se muda a config.py
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:@localhost/flask'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#Manejo de Migraciones de Base de Datos
migrate = Migrate(app, db)

#Aqui se importa la referencia Blue print de Usuarios
from Controladores.Usuarios_Controler import usuarios_bp
app.register_blueprint(usuarios_bp)

@app.route("/")
def inicio():    
    return render_template("Index.html")

@app.route("/lista_roles")
def lista_roles():
    roles_aplicacion = Rol_Aplicacion.query.order_by(Rol_Aplicacion.fecha_creacion.asc()).all() 
    return render_template("lista_roles.html", roles_aplicacion=roles_aplicacion)

@app.route("/nuevo_usuario_wtform", methods = ['GET', 'POST'])
def registrar_usuario():
    form = IngresaUsuario(request.form)
    if request.method ==  'POST' and form.validate():
        usuario =   Usuario(
                    nombres = form.nombres.data,
                    fk_rol  =  1,
                    apellido_paterno =  form.apellido_paterno.data,
                    apellido_materno =  form.apellido_materno.data,
                    correo =  form.correo.data,
                    contraseña =  form.contraseña.data,
                    telefono =  form.telefono.data,
                    estado =  True)
        db.session.add(usuario)
        db.session.commit()
        flash('Registro completo')
        return redirect("/")
    return render_template('nuevo_usuario_wtform.html', form=form)
 
if __name__ == "__main__":    
    app.run(debug=True)