
from app import User, Role
#Aqui se importa la creación de referencia BluePrint de Usuario
from . import usuarios_bp
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from .form_usuario import SignupForm, LoginForm
from werkzeug.urls import url_parse
from app import login_manager
from app import db


@usuarios_bp.route("/nuevo_usuario", methods = ['GET'])
def nuevo_usuario():
    roles_aplicacion = Role.query.order_by(Role.fecha_creacion.asc()).all()  
    return render_template("usuarios/nuevo_usuario.html", roles_aplicacion=roles_aplicacion)

@usuarios_bp.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST' :
        usuario                  = User.query.get(request.form.get('id'))        
        usuario.name             = request.form['nombres']
        usuario.apellido_paterno = request.form['apellido_paterno']
        usuario.apellido_materno = request.form['apellido_materno']
        usuario.email            = request.form['correo']
        usuario.fk_rol           = request.form['rol_aplicacion']
        usuario.password         = request.form['contraseña']
        if request.form.get('estado') == 'True':
            usuario.estado = 1
        if request.form.get('estado') != 'True':
            usuario.estado = 0
        db.session.merge(usuario)
        db.session.flush()
        db.session.commit()
        flash("Usuario actualizado")
 
        return redirect(url_for('usuarios.lista_usuarios'))

@usuarios_bp.route("/lista_usuarios")
def lista_usuarios():
    usuarios = User.query.order_by(User.fecha_creacion.asc()).all() 
    return render_template("usuarios/lista_usuarios.html", usuarios=usuarios)

@usuarios_bp.route("/nuevo_usuario", methods=["POST"])
def crear_usuario():
    nombres          = request.form.get("nombres")    
    fk_rol           = request.form.get("rol_aplicacion")
    apellido_paterno = request.form.get("apellido_paterno")
    apellido_materno = request.form.get("apellido_materno")
    correo           = request.form.get("correo")
    password       = request.form.get("contraseña")
    telefono         = request.form.get("telefono")
    estado           = True
    usuario          = User(name=nombres,
                            apellido_paterno=apellido_paterno,
                            fk_rol = fk_rol, 
                            apellido_materno=apellido_materno,
                            email=correo,
                            password=password,
                            telefono=telefono,
                            estado=estado)
    usuario.set_password(password)
    usuario.save()
    # Dejamos al usuario logueado
    login_user(usuario, remember=True) 
    return redirect("/")

# @usuarios_bp.route("/login_usuario", methods = ['GET'])
# def login_usuario():
#     return render_template("usuarios/login_usuario.html")

# @usuarios_bp.route("/logeo_usuario", methods = ['POST'])
# def login_usuario():

#     return render_template("Index.html")

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return render_template("Index.html")
    #form = LoginForm()
    correo   = request.form.get("Email")
    password = request.form.get("Password")
    user = User.get_by_email(correo)
    if user is not None and user.check_password(password):
        login_user(user)
        return render_template("Index.html")
    # if form.validate_on_submit():
    #     user = Usuario.get_by_email(form.email.data)
    #     if user is not None and user.check_password(form.password.data):
    #         # login_user(user, remember=form.remember_me.data)
    #         login_user(user)
    #         return render_template("Index.html")
    return render_template('usuarios/login_usuario.html')

@usuarios_bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))