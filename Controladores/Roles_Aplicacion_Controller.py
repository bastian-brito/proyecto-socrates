
#from Modelo.Modelos import Role
#Aqui se importa la creación de referencia BluePrint de Usuario
from . import roles_aplicacion_bp
from flask import render_template, request, redirect,flash
from app import db, Role




@roles_aplicacion_bp.route("/lista_roles", methods = ['GET'])
def lista_roles():
    roles_aplicacion = Role.query.order_by(Role.fecha_creacion.asc()).all()  
    return render_template("lista_roles.html", roles_aplicacion=roles_aplicacion)

@roles_aplicacion_bp.route('/actualizar_rol', methods = ['GET', 'POST'])
def actualizar_rol():
 
    if request.method == 'POST' :
        rol_aplicacion                = Role.query.get(request.form.get('id'))        
        rol_aplicacion.nombres        = request.form.get('nombres', False)
        rol_aplicacion.descripcion    = request.form.get("descripcion", False)
        rol_aplicacion.fecha_creacion = request.form.get("fecha_creacion", False)
        if request.form.get('estado') == 'True':
            rol_aplicacion.estado     = 1
        if request.form.get('estado') != 'True':
            rol_aplicacion.estado     = 0
        db.session.merge(rol_aplicacion)
        db.session.flush()
        db.session.commit()
        flash("Rol actualizado")
 
        return redirect('/lista_roles')
    roles_aplicacion = Role.query.order_by(Role.fecha_creacion.asc()).all() 
    return render_template("lista_roles.html", roles_aplicacion=roles_aplicacion)

@roles_aplicacion_bp.route('/crear_rol', methods = ['POST'])    
def crear_rol():
    nombres        = request.form.get("nombres", False)    
    descripcion    = request.form.get("descripcion")
    estado         = True
    rol_aplicacion = Role(name=nombres,
                          descripcion=descripcion,
                          estado=estado)
    db.session.add(rol_aplicacion)
    db.session.commit()
    return redirect("/lista_roles")
