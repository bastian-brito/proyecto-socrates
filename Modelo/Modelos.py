# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 17:49:37 2021

@author: franc
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Rol_Aplicacion(db.Model):
    __tablename__  = "roles_aplicacion"
    id             = db.Column(db.Integer, primary_key=True)
    nombres        = db.Column(db.String(30), nullable=False)
    descripcion    = db.Column(db.String(60), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado         = db.Column(db.Boolean, nullable=False)
    usuarios       = db.relationship('Usuario', backref='roles_aplicacion', lazy=True)


class Red_Social(db.Model):
    __tablename__ = "redes_sociales"
    id             = db.Column(db.Integer, primary_key=True)
    nombre         = db.Column(db.String(60), nullable=False)    
    descripcion    = db.Column(db.String(60), nullable=False)
    link           = db.Column(db.String(60), nullable=False)    
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado         = db.Column(db.Boolean, nullable=False)
    usuarios       = db.relationship('Usuario_Red_Social', backref='redes_sociales', lazy=True)

class Usuario(db.Model):
    __tablename__    = "usuarios"
    id               = db.Column(db.Integer, primary_key=True)
    nombres          = db.Column(db.String(60), nullable=False)
    fk_rol           = db.Column(db.Integer, db.ForeignKey('roles_aplicacion.id'), nullable=False)
    apellido_paterno = db.Column(db.String(30), nullable=False)
    apellido_materno = db.Column(db.String(30), nullable=False)
    correo           = db.Column(db.String(60), unique=True)
    contraseña       = db.Column(db.String(60), nullable=False)
    telefono         = db.Column(db.Integer, nullable=False)
    fecha_creacion   = db.Column(db.DateTime, default=datetime.now)
    estado           = db.Column(db.Boolean, nullable=False)
    red_socials      = db.relationship('Usuario_Red_Social', backref='usuarios', lazy=True)

class Usuario_Red_Social(db.Model):
    __tablename__  = "usuarios_redes_sociales"
    fk_usuario     = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    fk_red_social  = db.Column(db.Integer, db.ForeignKey('redes_sociales.id'), primary_key=True)      
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado         = db.Column(db.Boolean, nullable=False)