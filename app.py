from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from Modelo.Modelos import *

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:@localhost/flask'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/")
def inicio():    
    return render_template("Index.html")

@app.route("/nuevo_usuario")
def nuevo_usuario():    
    return render_template("nuevo_usuario.html")

#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        usuario = Usuario.query.get(request.form.get('id'))
 
        usuario.nombres = request.form['nombres']
        usuario.apellido_paterno = request.form['apellido_paterno']
        usuario.correo = request.form['correo']
        db.session.merge(usuario)
        db.session.flush()
        db.session.commit()
        flash("Usuario actualizado")
 
        return redirect(url_for('lista_usuarios'))

@app.route("/lista_usuarios")
def lista_usuarios():
    usuarios = Usuario.query.order_by(Usuario.fecha_creacion.asc()).all() 
    return render_template("lista_usuarios.html", usuarios=usuarios)


@app.route("/nuevo_usuario", methods=["POST"])
def crear_usuario():
    nombres          = request.form.get("nombres")    
    fk_rol           = 1
    apellido_paterno = request.form.get("apellido_paterno")
    apellido_materno = request.form.get("apellido_materno")
    correo           = request.form.get("correo")
    contraseña       = request.form.get("contraseña")
    telefono         = request.form.get("telefono")
    estado           = True
    usuario          = Usuario(nombres=nombres,
                            apellido_paterno=apellido_paterno,
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