# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 17:49:37 2021

@author: franc
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
#from app import db
from __main__ import db


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
    #Agregar nombre de usuario, aparte de nombre propio
    name             = db.Column(db.String(80), nullable=False)    
    apellido_paterno = db.Column(db.String(30), nullable=False)
    apellido_materno = db.Column(db.String(30), nullable=False)
    email            = db.Column(db.String(256), unique=True, nullable=True)    
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
        
    """ """
    #Se consulta por si Usuario tiene algun rol
    """ """    
    def has_role(self, rol):
        return any(rol == role.name for role in self.roles)
    
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
    __tablename__  = 'user_roles'
    id             = db.Column(db.Integer(), primary_key=True)
    user_id        = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id        = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado         = db.Column(db.Boolean, nullable=False)

class Usuario_Red_Social(db.Model):
    __tablename__  = "usuarios_redes_sociales"
    fk_usuario     = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    fk_red_social  = db.Column(db.Integer(), db.ForeignKey('redes_sociales.id'), primary_key=True)      
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado         = db.Column(db.Boolean, nullable=False)

class Escuela(db.Model):
    __tablename__   = 'escuelas'
    id              = db.Column(db.Integer(), primary_key=True)
    name            = db.Column(db.String(30), nullable=False)
    user_id         = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    fecha_creacion  = db.Column(db.DateTime, default=datetime.now)
    publicado       = db.Column(db.Boolean, nullable=False)
    estado          = db.Column(db.Boolean, nullable=False)
    planes_escuelas = db.relationship('Plan', secondary='planes_escuelas')

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

#Cambio nombre de clase desde Plan a Suscripcion
class Suscripcion(db.Model):
    __tablename__   = 'suscripciones'
    id              = db.Column(db.Integer(), primary_key=True)
    #No ocupa esta relación mala relacion por eso la Quite
    #escuela_id      = db.Column(db.Integer(), db.ForeignKey('escuelas.id', ondelete='CASCADE'))
    fecha_creacion  = db.Column(db.DateTime, default=datetime.now)
    publicado       = db.Column(db.Boolean, nullable=False)
    name            = db.Column(db.String(30), nullable=False)
    precio          = db.Column(db.String(30), nullable=False)
    #Cambio nombre de columna descripcion a Tipo
    tipo            = db.Column(db.String(60), nullable=False)
    #Cambio nombre de columna caracteristicas a Nivel
    nivel           = db.Column(db.String(60), nullable=False)
    estado          = db.Column(db.Boolean, nullable=False)
    planes_escuelas = db.relationship('Escuela', secondary='planes_escuelas')

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

#Cambio nombre Plan_Escuela a Suscripcion_Escuela
class Suscripcion_Escuela(db.Model):
    __tablename__    = 'suscripciones_escuelas'
    id               = db.Column(db.Integer(), primary_key=True)
    plan_id          = db.Column(db.Integer(), db.ForeignKey('planes.id', ondelete='CASCADE'))
    escuela_id       = db.Column(db.Integer(), db.ForeignKey('escuelas.id', ondelete='CASCADE'))
    fecha_creacion   = db.Column(db.DateTime, default=datetime.now)    
    estado           = db.Column(db.Boolean, nullable=False)
    validez_contrato = db.Column(db.String(60), nullable=False)
    pago_escuela     = db.relationship('Pago_Escuela', backref='planes_escuelas', lazy=True)
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Pago_Escuela(db.Model):
    __tablename__       = 'pagos_escuelas'
    id                  = db.Column(db.Integer(), primary_key=True)
    planes_escuelas_id  = db.Column(db.Integer(), db.ForeignKey('planes_escuelas.id', ondelete='CASCADE'))
    numero_pago         = db.Column(db.Integer, nullable=False)
    fecha_creacion      = db.Column(db.DateTime, default=datetime.now)
    #Cuando se debe cobrar el pago
    # Ejemplo start_date = datetime.datetime.now() - datetime.timedelta(30)
    fecha_cobro         = db.Column(db.DateTime, nullable=False)
    #Cuando se pago efectivamente
    fecha_pago          = db.Column(db.DateTime, nullable=False)
    publicado           = db.Column(db.Boolean, nullable=False)
    estado_pago         = db.Column(db.String(60), nullable=False)
    estado              = db.Column(db.Boolean, nullable=False)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Alumno(db.Model):
    __tablename__       = 'alumnos'
    id                  = db.Column(db.Integer(), primary_key=True)
    usuario_id          = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    escuela_id          = db.Column(db.Integer(), db.ForeignKey('escuelas.id', ondelete='CASCADE'))
    fecha_creacion      = db.Column(db.DateTime, default=datetime.now)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Curso(db.Model):
    __tablename__       = 'cursos'
    id                  = db.Column(db.Integer(), primary_key=True)    
    escuela_id          = db.Column(db.Integer(), db.ForeignKey('escuelas.id', ondelete='CASCADE'))
    fecha_creacion      = db.Column(db.DateTime, default=datetime.now)
    name                = db.Column(db.String(30), nullable=False)
    descripcion         = db.Column(db.String(60), nullable=False)
    estado              = db.Column(db.Boolean, nullable=False)

class Tag(db.Model):
    __tablename__       = 'tags'
    id                  = db.Column(db.Integer(), primary_key=True)
    fecha_creacion      = db.Column(db.DateTime, default=datetime.now)
    name                = db.Column(db.String(30), nullable=False)
    estado              = db.Column(db.Boolean, nullable=False)