from wtforms import Form
from wtforms import StringField, PasswordField, validators, IntegerField, SelectField
from wtforms.validators import ValidationError
from wtforms.fields.html5 import EmailField
from Modelo.Modelos import User, Role

def validate_email_2(form, field):
	user = User.query.filter_by(email=field.data).first()
	if user is not None:
		raise ValidationError('Email Malulo')

class IngresaUsuario(Form):
	correo           	=	EmailField("correo electrónico",validators = [validators.InputRequired(),validate_email_2])
	nombres          	=	StringField("Nombres")
	apellido_paterno 	=	StringField("Apellido Paterno")
	apellido_materno 	=	StringField("Apellido Materno")
	telefono		 	=	IntegerField("Teléfono")
	roles				=	SelectField(u'Rol', coerce=int, validate_choice=True)
	contraseña       	=	PasswordField("Nueva Contraseña",validators = [validators.InputRequired()], id="contraseña")
	confirma_contraseña =	PasswordField("Repite la Contraseña",validators = [validators.InputRequired(),
		validators.EqualTo("contraseña", message="Contraseñas deben coincidir")],
		id="confirma_contraseña")
	estado				=	True

def validate_email(self, correo):
	user = User.query.filter_by(email=correo.data).first()
	if user is not None:
		raise ValidationError('Porfavor use una diferente dirección de email.')

def lista_roles(request, id):
	roles = Role.query.order_by(Role.fecha_creacion.asc()).all() 
	form = IngresaUsuario(request.POST, obj=roles)
	form.roles.choices = [(role.id, role.name) for role in roles]

