from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from Modelo.Modelos import *
from formulario import IngresaUsuario

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

# @app.route("/nuevo_usuario_wtform")
# def nuevo_usuario_wtform():    
#     return render_template("nuevo_usuario_wtform.html")
#tenalsndlasd

#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST' :
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