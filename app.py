from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from Modelo.Modelos import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:@localhost/flask'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def inicio():    
    return render_template("Index.html")

#this is our update route where we are going to update our employee

@app.route("/lista_usuarios")
def lista_usuarios():
    usuarios = Usuario.query.order_by(Usuario.fecha_creacion.asc()).all() 
    return render_template("lista_usuarios.html", usuarios=usuarios)

@app.route("/editar_usuario/<int:id>", methods=['POST','GET'] )
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == "POST":
        #usuario.nombres = request.form['nombres']
        usuario.nombres = request.form.get("nombres") 
        usuario.apellido_paterno = request.form.get("apellido_paterno")
        usuario.apellido_materno = request.form.get("apellido_materno")
        usuario.correo = request.form.get("correo")
        usuario.contraseña= request.form.get("contraseña")
        usuario.telefono = request.form.get("telefono")
        try:
            db.session.merge(usuario)
            db.session.flush()
            db.session.commit()
            return redirect('/lista_usuarios')
        except: 
            return "error al actualizar"
    else:
        return render_template('editar_usuario.html', usuario=usuario)
        

    return render_template("editar_usuario.html", )

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