# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 17:49:37 2021

@author: franc
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(60), nullable=False)

    fk_rol = db.Column(db.Integer, db.ForeignKey('roles_aplicacion.id'), nullable=False)
    roles_aplicacion = db.relationship(Rol_Aplicacion, backref=backref('usuarios', uselist=True)) 

    apellido_paterno = db.Column(db.String(30), nullable=False)
    apellido_materno = db.Column(db.String(30), nullable=False)
    correo = db.Column(db.String(60), unique=True)
    contraseña= db.Column(db.String(60), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado = db.Column(db.Boolean, nullable=False)
    red_socials = db.relationship('redes_sociales', secondary='usuarios_redes_sociales')


