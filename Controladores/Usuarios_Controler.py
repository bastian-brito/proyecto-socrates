
from Modelo.Modelos import Usuario
#Aqui se importa la creación de referencia BluePrint de Usuario
from . import usuarios_bp
from flask import render_template, request, redirect, url_for
from app import db


@usuarios_bp.route("/nuevo_usuario")
def nuevo_usuario():    
    return render_template("usuarios/nuevo_usuario.html")

@usuarios_bp.route('/update', methods = ['GET', 'POST'])
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

@usuarios_bp.route("/lista_usuarios")
def lista_usuarios():
    usuarios = Usuario.query.order_by(Usuario.fecha_creacion.asc()).all() 
    return render_template("usuarios/lista_usuarios.html", usuarios=usuarios)

@usuarios_bp.route("/nuevo_usuario", methods=["POST"])
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