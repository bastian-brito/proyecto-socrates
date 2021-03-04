from Modelo.Modelos import Escuela, User
from . import escuelas_bp
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from functools import wraps
from app import login_manager
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

#@roles_required(['Admin'])
@escuelas_bp.route("/lista_escuelas", methods = ['GET','POST'])
def lista_escuelas():
    escuelas = Escuela.query.order_by(Escuela.fecha_creacion.asc()).all()
    return render_template("escuelas/lista_escuelas.html", escuelas=escuelas)

@escuelas_bp.route("/nueva_escuela", methods = ['GET'])
def nueva_escuela():
	#if current_user.is_authenticated:
	return render_template("escuelas/nueva_escuela.html")

#@roles_required(['Admin'])
@escuelas_bp.route("/nueva_escuela", methods=["POST"])
def crear_escuela():
	if current_user.is_authenticated:
		name      = request.form.get("name")
		user_id   = current_user.get_id()
		publicado = True
		estado    = True
		escuela   = Escuela(name=name,
                            user_id=user_id,	                             
                            publicado=publicado,	                            
                            estado=estado)
		escuela.save()
		return redirect("/")
	return redirect("/login")

@escuelas_bp.route('/escuela_update', methods = ['GET', 'POST'])
def escuela_update():
    
    escuela                  = Escuela.query.get(request.form.get('id'))        
    escuela.name             = request.form['name']    
    if request.form.get('estado') == 'True':
        escuela.estado = 1
    if request.form.get('estado') != 'True':
        escuela.estado = 0
    escuela.save()
    #db.session.merge(escuela)
    #db.session.flush()
    #db.session.commit()
    flash("Escuela actualizada")

    return redirect(url_for('escuelas.lista_escuelas'))

#@escuelas_bp.route('/escuela_profile',  subdomain = "<escuela>",  methods=['GET', 'POST'])
#def escuela_profile(escuela):
#	escuela = Escuela.query.filter_by(name='escuela').first()
#	return render_template("escuelas/escuela_profile.html", escuela=escuela)

@escuelas_bp.route("/dynamic", subdomain="<escuela>")
def escuela_profile(escuela):
    """Dynamic subdomains are also supported
    Try going to user1.your-domain.tld/dynamic"""
    return escuela + ".sitio.tld"


#@app.route("/dynamic", subdomain="<username>")
#def username_index(username):
    """Dynamic subdomains are also supported
    Try going to user1.your-domain.tld/dynamic"""
#    return username + ".your-domain.tld"


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))