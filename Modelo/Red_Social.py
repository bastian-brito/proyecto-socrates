# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 17:49:37 2021

@author: franc
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Red_Social(db.Model):
    __tablename__ = "redes_sociales"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)    
    descripcion = db.Column(db.String(60), nullable=False)
    link = db.Column(db.String(60), nullable=False)    
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado = db.Column(db.Boolean, nullable=False)
    usuarios = db.relationship('Usuario', secondary='usuarios_redes_sociales')




