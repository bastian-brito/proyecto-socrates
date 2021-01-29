
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Usuario_Red_Social(db.Model):
    __tablename__ = "usuarios_redes_sociales"
    fk_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    fk_red_social = db.Column(db.Integer, db.ForeignKey('usuario_red_social.id'), primary_key=True)      
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado = db.Column(db.Boolean, nullable=False)


