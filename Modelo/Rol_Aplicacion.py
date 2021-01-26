# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 17:33:55 2021

@author: franc
"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Rol_Aplicacion(db.Model):
    __tablename__ = "roles_aplicacion"
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.String(60), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    usuarios = db.relationship('Usuario', backref='roles_aplicacion', lazy=True)