
from Modelo.Modelos import Red_Social
#Aqui se importa la creación de referencia BluePrint de Usuario
from . import redes_sociales_bp
from flask import render_template, request, redirect,flash
from app import db


@roles_aplicacion_bp.route("/lista_redes_sociales", methods = ['GET'])
def lista_roles():
    roles_aplicacion = Rol_Aplicacion.query.order_by(Rol_Aplicacion.fecha_creacion.asc()).all()  
    return render_template("lista_roles.html", roles_aplicacion=roles_aplicacion)

@roles_aplicacion_bp.route('/lista_roles', methods = ['GET', 'POST'])
def update_rol():
 
    if request.method == 'POST' and request.form['editar']:
        rol_aplicacion                = Rol_Aplicacion.query.get(request.form.get('id'))        
        rol_aplicacion.nombres        = request.form['nombres']
        rol_aplicacion.descripcion    = request.form['descripcion']
        rol_aplicacion.fecha_creacion = request.form['fecha_creacion']
        if request.form.get('estado') == 'True':
            rol_aplicacion.estado     = 1
        if request.form.get('estado') != 'True':
            rol_aplicacion.estado     = 0
        db.session.merge(rol_aplicacion)
        db.session.flush()
        db.session.commit()
        flash("Rol actualizado")
 
        return redirect('/lista_roles')

@roles_aplicacion_bp.route('/crear_rol', methods = ['GET', 'POST'])   
def crear_rol():

    if request.method == 'POST':
        nombres        = request.form.get("nombre_nuevo")    
        descripcion    = request.form.get("descripcion_nuevo")
        estado         = True
        rol_aplicacion = Rol_Aplicacion(nombres=nombres,
                                    descripcion=descripcion,
                                    estado=estado)
        db.session.add(rol_aplicacion)
        db.session.commit()
        return redirect("/lista_roles")

# @roles_aplicacion_bp.route("/lista_roles")
# def lista_roles():
#     roles_aplicacion = Rol_Aplicacion.query.order_by(Rol_Aplicacion.fecha_creacion.asc()).all() 
#     return render_template("lista_roles.html", roles_aplicacion=roles_aplicacion)

# @roles_aplicacion_bp.route("/nuevo_usuario", methods=["POST"])
# def crear_usuario():
#     nombres          = request.form.get("nombres")    
#     fk_rol           = request.form.get("rol_aplicacion")
#     apellido_paterno = request.form.get("apellido_paterno")
#     apellido_materno = request.form.get("apellido_materno")
#     correo           = request.form.get("correo")
#     contraseña       = request.form.get("contraseña")
#     telefono         = request.form.get("telefono")
#     estado           = True
#     usuario          = Usuario(nombres=nombres,
#                             apellido_paterno=apellido_paterno,
#                             fk_rol = fk_rol, 
#                             apellido_materno=apellido_materno,
#                             correo=correo,
#                             contraseña=contraseña,
#                             telefono=telefono,
#                             estado=estado)
#     db.session.add(usuario)
#     db.session.commit()
#     return redirect("/")