from wtforms import Form
from wtforms import StringField, PasswordField, validators, IntegerField, BooleanField
from wtforms.fields.html5 import EmailField

class IngresaUsuario(Form):
		correo           	=	EmailField("correo electrónico")
		nombres          	=	StringField("Nombres")
		apellido_paterno 	=	StringField("Apellido Paterno")
		apellido_materno 	=	StringField("Apellido Materno")
		telefono		 	=	IntegerField("Teléfono")
		contraseña       	=	PasswordField("Nueva Contraseña",validators = [validators.InputRequired()], id="contraseña")
		confirma_contraseña =	PasswordField("Repite la Contraseña",validators = [validators.InputRequired(),
									validators.EqualTo("contraseña", message="Contraseñas deben coincidir")],
									id="confirma_contraseña")
		fk_rol				=	1
		estado				=	BooleanField("estado")
