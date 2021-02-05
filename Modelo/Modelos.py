# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 17:49:37 2021

@author: franc
"""

from datetime import datetime
#from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Red_Social(db.Model):
    __tablename__ = "redes_sociales"
    id             = db.Column(db.Integer, primary_key=True)
    nombre         = db.Column(db.String(60), nullable=False)    
    descripcion    = db.Column(db.String(60), nullable=False)
    link           = db.Column(db.String(60), nullable=False)    
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado         = db.Column(db.Boolean, nullable=False)
    usuarios       = db.relationship('Usuario_Red_Social', backref='redes_sociales', lazy=True)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String(80), nullable=False)    
    apellido_paterno = db.Column(db.String(30), nullable=False)
    apellido_materno = db.Column(db.String(30), nullable=False)
    email            = db.Column(db.String(256), unique=True, nullable=False)
    password         = db.Column(db.String(128), nullable=False)
    telefono         = db.Column(db.Integer, nullable=False)
    fecha_creacion   = db.Column(db.DateTime, default=datetime.now)
    estado           = db.Column(db.Boolean, nullable=False)
    red_socials      = db.relationship('Usuario_Red_Social', backref='users', lazy=True)
    roles            = db.relationship('Role', secondary='user_roles')

    def __repr__(self):
        return f'<Usuario {self.email}>'
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

class Role(db.Model):
    __tablename__  = "roles"
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(30), nullable=False)
    descripcion    = db.Column(db.String(60), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado         = db.Column(db.Boolean, nullable=False)
    users          = db.relationship('User', secondary='user_roles')

class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id             = db.Column(db.Integer(), primary_key=True)
        user_id        = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        role_id        = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
        fecha_creacion = db.Column(db.DateTime, default=datetime.now)
        estado         = db.Column(db.Boolean, nullable=False)

class Usuario_Red_Social(db.Model):
    __tablename__  = "usuarios_redes_sociales"
    fk_usuario     = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    fk_red_social  = db.Column(db.Integer, db.ForeignKey('redes_sociales.id'), primary_key=True)      
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado         = db.Column(db.Boolean, nullable=False)