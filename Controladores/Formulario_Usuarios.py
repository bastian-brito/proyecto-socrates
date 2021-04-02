from wtforms import Form
from wtforms import StringField, PasswordField, validators, IntegerField, SelectField, HiddenField
from wtforms.validators import ValidationError
from wtforms.fields.html5 import EmailField
from Modelo.Modelos import User, Role, UserRoles
from flask_table import Table, Col, NestedTableCol, LinkCol, ButtonCol

def validate_email_2(form, field):
	user = User.query.filter_by(email=field.data).first()
	if user is not None:
		raise ValidationError('Email ya en uso')

def validate_email_update(form, field):
	user_test = User.query.filter_by(email=field.data).first()
	#current_user.
	user = User.query.get(form.id.data)
	if user != field.data:
		if user_test is not None:
			raise ValidationError('Email ya en uso')

class ListaRoles(Table):
	name = Col('')

#csrf_token = csrf_token()

class ListaUsuarios(Table):
	# modaledit = '#modaledit'+usuario.id
	id = Col('ID')
	name = Col('Nombres')
	apellido_paterno = Col('Apellido Paterno')
	apellido_materno = Col('Apellido Materno')
	roles = NestedTableCol('Roles', ListaRoles)
	email = Col('Correo')
	#password = Col('Contraseña')
	telefono = Col('Teléfono')
	estado = Col('Estado')
	acción = LinkCol('Acción', 'usuarios.update_wtf', url_kwargs=dict(id='id'), anchor_attrs={'class': 'btn btn-warning btn-xs'})

class ItemUsuario(object):
	def __init__(self, name, apellido_paterno, apellido_materno, roles, email, telefono, estado):
		self.id = id
		self.name = name
		self.apellido_paterno = apellido_paterno
		self.apellido_materno = apellido_materno
		self.roles = roles.name
		self.email = email
		self.telefono = telefono
		self.estado = estado


class IngresaUsuario(Form):


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.roles.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]


	correo           	=	EmailField("correo electrónico", validators = [validators.InputRequired(),validate_email_2])
	nombres          	=	StringField("Nombres")
	apellido_paterno 	=	StringField("Apellido Paterno")
	apellido_materno 	=	StringField("Apellido Materno")
	telefono		 	=	IntegerField("Teléfono")
	roles				=	SelectField('Rol', choices=[], coerce=int)
	contraseña       	=	PasswordField("Nueva Contraseña", validators = [validators.InputRequired()], id="contraseña")
	confirma_contraseña =	PasswordField("Repite la Contraseña", validators = [validators.InputRequired(),
		validators.EqualTo("contraseña", message="Contraseñas deben coincidir")],
		id="confirma_contraseña")
	estado				=	True

class EditaUsuario(Form):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#self.roles.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]

	id 					= 	HiddenField('ID')
	# email         	  	=	EmailField("Correo electrónico", validators = [validators.InputRequired(),validate_email_update])
	email         	  	=	EmailField("Correo electrónico", validators = [validators.InputRequired()])
	name          		=	StringField("Nombres")
	apellido_paterno 	=	StringField("Apellido Paterno")
	apellido_materno 	=	StringField("Apellido Materno")
	telefono		 	=	IntegerField("Teléfono")
	#roles				=	SelectField('Rol', choices=[], coerce=int)
	#contraseña       	=	PasswordField("Nueva Contraseña", id="contraseña")
	#confirma_contraseña =	PasswordField("Repite la Contraseña", validators = [validators.EqualTo("contraseña", message="Contraseñas deben coincidir")],
	#	id="confirma_contraseña")
	#estado				=	True

