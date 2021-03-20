
from Modelo.Modelos import User, Role
#Aqui se importa la creación de referencia BluePrint de Usuario
from . import usuarios_bp
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from functools import wraps
from formulario import IngresaUsuario
#formulario
#from .form_usuario import SignupForm, LoginForm
#from werkzeug.urls import url_parse
from app import login_manager
#from app import db
#from __main__ import db

def roles_required(roles: list, require_all=False):
    def _roles_required(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if len(roles) == 0:
                raise ValueError('Empty list used when requiring a role.')
            if not current_user.is_authenticated:
                #return login_manager.unauthorized()
                return redirect("/login")
            if require_all and not all(current_user.has_role(role) for role in roles):
                #Poner direcciones de retorno correctas (mantenerme en la misma pagina o retornar index)
                #return 'Forbidden1', 403
                return redirect("/login")
            elif not require_all and not any(current_user.has_role(role) for role in roles):
                #Poner direcciones de retorno correctas (mantenerme en la misma pagina o retornar index)
                #return 'Forbidden2', 403
                return redirect("/login")
            return f(*args, **kwargs)
        return decorated_view
    return _roles_required

@roles_required(['Admin'])
@usuarios_bp.route("/nuevo_usuario", methods = ['GET'])
def nuevo_usuario():
    roles = Role.query.order_by(Role.fecha_creacion.asc()).all()  
    return render_template("usuarios/nuevo_usuario.html", roles=roles)

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
        usuario.set_password(usuario.password)
        usuario.save()        
        flash("Usuario actualizado")
 
        return redirect(url_for('usuarios.lista_usuarios'))


@usuarios_bp.route("/lista_usuarios", methods = ['GET'])
@roles_required(['Admin'])
def lista_usuarios():
    usuarios = User.query.order_by(User.fecha_creacion.asc()).all() 
    return render_template("usuarios/lista_usuarios.html", usuarios=usuarios)

@usuarios_bp.route("/nuevo_usuario", methods=["POST"])
@roles_required(['Admin'])
def crear_usuario():
    nombres          = request.form.get("nombres")  
    apellido_paterno = request.form.get("apellido_paterno")
    apellido_materno = request.form.get("apellido_materno")
    correo           = request.form.get("correo")
    password        = request.form.get("contraseña")
    telefono         = request.form.get("telefono")
    estado           = True
    usuario          = User(name=nombres,
                            apellido_paterno=apellido_paterno,
                            #fk_rol = fk_rol, 
                            apellido_materno=apellido_materno,
                            email=correo,
                            password=password,
                            telefono=telefono,
                            estado=estado)
    #admin_role = Role(name='Admin')
    admin_role = Role.query.get(1)
    user_role = Role.query.get(2)   
    usuario.roles = [admin_role, user_role, ]
    usuario.set_password(password)
    usuario.save()
    # Dejamos al usuario logueado
    login_user(usuario, remember=True) 
    return redirect("/")

@usuarios_bp.route("/nuevo_usuario_wtform", methods = ['GET', 'POST'])
def registrar_usuario():
    form = IngresaUsuario(request.form)    
    if request.method ==  'POST' and form.validate():
        usuario =   User(                
                    name = form.nombres.data,                    
                    apellido_paterno =  form.apellido_paterno.data,
                    apellido_materno =  form.apellido_materno.data,
                    email =  form.correo.data,
                    password =  form.contraseña.data,
                    telefono =  form.telefono.data,
                    estado =  True)
        admin_role = Role.query.get(1)
        user_role = Role.query.get(2)  
        usuario.roles = [admin_role, user_role, ]
        usuario.set_password(usuario.password)
        usuario.save()
        # Dejamos al usuario logueado
        login_user(usuario, remember=True)        
        flash('Registro completo')
        return redirect("/")      
    return render_template('nuevo_usuario_wtform.html', form=form)

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return render_template("Index.html")    
    correo   = request.form.get("Email")
    password = request.form.get("Password")
    user = User.get_by_email(correo)
    if user is not None and user.check_password(password):
        login_user(user)
        return render_template("Index.html")    
    return render_template('usuarios/login_usuario.html')

@usuarios_bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

