from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:@localhost/flask'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Rol_Aplicacion(db.Model):
    __tablename__ = "roles_aplicacion"
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.String(60), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    usuarios = db.relationship('Usuario', backref='roles_aplicacion', lazy=True)
    

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(60), nullable=False)
    fk_rol = db.Column(db.Integer, db.ForeignKey('roles_aplicacion.id'), nullable=False)
    apellido_paterno = db.Column(db.String(30), nullable=False)
    apellido_materno = db.Column(db.String(30), nullable=False)
    correo = db.Column(db.String(60), unique=True)
    contraseña= db.Column(db.String(60), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado = db.Column(db.Boolean, nullable=False)


@app.route("/")
def inicio():	 
	return render_template("Index.html")

@app.route("/crear", methods=["POST"])
def crear_usuario():
    nombres = request.form.get("nombres")    
    fk_rol = 1
    apellido_paterno = request.form.get("apellido_paterno")
    apellido_materno = request.form.get("apellido_materno")
    correo = request.form.get("correo")
    contraseña= request.form.get("contraseña")
    telefono = request.form.get("telefono")
    estado = True
    usuario = Usuario(nombres=nombres, apellido_paterno=apellido_paterno,
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