from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from Modelo.Modelos import *
#from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:@localhost/flask'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route("/")
def inicio():    
    return render_template("Index.html")

@app.route("/nuevo_usuario")
def nuevo_usuario():    
    return render_template("nuevo_usuario.html")

@app.route("/nuevo_usuario", methods=["POST"])
def crear_usuario():
    nombres = request.form.get("nombres")    
    fk_rol = 1
    apellido_paterno = request.form.get("apellido_paterno")
    apellido_materno = request.form.get("apellido_materno")
    correo = request.form.get("correo")
    contraseña= request.form.get("contraseña")
    telefono = request.form.get("telefono")
    estado = True
    usuario = Usuario(nombres=nombres, apellido_paterno=apellido_paterno,
                     fk_rol = fk_rol, 
                     apellido_materno=apellido_materno,
                     correo=correo,
                     contraseña=contraseña,
                     telefono=telefono,
                     estado=estado)
    db.session.add(usuario)
    db.session.commit()
    return redirect("/")
 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)