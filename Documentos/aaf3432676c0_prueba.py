"""Prueba

Revision ID: aaf3432676c0
Revises: c4fa4b2ac064
Create Date: 2021-02-05 13:54:41.039797

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'aaf3432676c0'
down_revision = 'c4fa4b2ac064'
branch_labels = None
depends_on = None


def upgrade():
    
    # Inicio edición de cambios

    op.rename_table('roles_aplicacion', 'roles')
    op.alter_column('roles','nombres', new_column_name='name', existing_type=sa.String(30))

    op.rename_table('usuarios', 'users')
    op.alter_column('users', 'nombres', new_column_name='name', existing_type=sa.String(80))
    op.alter_column('users', 'correo', new_column_name='email', existing_type=sa.String(256))
    op.alter_column('users', 'contraseña', new_column_name='password', existing_type=sa.String(128))


    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    sa.Column('estado', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('usuarios_redes_sociales_ibfk_2', 'usuarios_redes_sociales', type_='foreignkey')
    op.create_foreign_key(None, 'usuarios_redes_sociales', 'users', ['fk_usuario'], ['id'])

    # fin edicion de cambios / inicio cambios originales

    # ### commands auto generated by Alembic - please adjust! ###

    # op.create_table('roles',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('name', sa.String(length=30), nullable=False),
    # sa.Column('descripcion', sa.String(length=60), nullable=False),
    # sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    # sa.Column('estado', sa.Boolean(), nullable=False),
    # sa.PrimaryKeyConstraint('id')
    # )
    # op.create_table('users',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('name', sa.String(length=80), nullable=False),
    # sa.Column('apellido_paterno', sa.String(length=30), nullable=False),
    # sa.Column('apellido_materno', sa.String(length=30), nullable=False),
    # sa.Column('email', sa.String(length=256), nullable=False),
    # sa.Column('password', sa.String(length=128), nullable=False),
    # sa.Column('telefono', sa.Integer(), nullable=False),
    # sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    # sa.Column('estado', sa.Boolean(), nullable=False),
    # sa.PrimaryKeyConstraint('id'),
    # sa.UniqueConstraint('email')
    # )
    # op.create_table('user_roles',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('user_id', sa.Integer(), nullable=True),
    # sa.Column('role_id', sa.Integer(), nullable=True),
    # sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    # sa.Column('estado', sa.Boolean(), nullable=False),
    # sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    # sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    # sa.PrimaryKeyConstraint('id')
    # )
    # op.drop_index('correo', table_name='usuarios')
    # op.drop_table('usuarios')
    # op.drop_table('roles_aplicacion')
    # op.drop_constraint('usuarios_redes_sociales_ibfk_2', 'usuarios_redes_sociales', type_='foreignkey')
    # op.create_foreign_key(None, 'usuarios_redes_sociales', 'users', ['fk_usuario'], ['id'])
    # ### end Alembic commands ###


def downgrade():

    op.rename_table('roles','roles_aplicacion')
    op.alter_column('roles_aplicacion','name', new_column_name='nombres', existing_type=sa.String(30))

    op.rename_table('users', 'usuarios')
    op.alter_column('usuarios', 'name', new_column_name='nombres', existing_type=sa.String(80))
    op.alter_column('usuarios', 'email', new_column_name='correo', existing_type=sa.String(256))
    op.alter_column('usuarios', 'password', new_column_name='contraseña', existing_type=sa.String(128))

    op.drop_table('user_roles')

    op.drop_constraint('usuarios_redes_sociales_ibfk_2', 'usuarios_redes_sociales', type_='foreignkey')
    op.create_foreign_key(None, 'usuarios_redes_sociales', 'usuarios', ['fk_usuario'], ['id'])


    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint(None, 'usuarios_redes_sociales', type_='foreignkey')
    # op.create_foreign_key('usuarios_redes_sociales_ibfk_2', 'usuarios_redes_sociales', 'usuarios', ['fk_usuario'], ['id'])
    # op.create_table('roles_aplicacion',
    # sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    # sa.Column('nombres', mysql.VARCHAR(length=30), nullable=False),
    # sa.Column('descripcion', mysql.VARCHAR(length=60), nullable=False),
    # sa.Column('fecha_creacion', mysql.DATETIME(), nullable=True),
    # sa.Column('estado', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    # sa.CheckConstraint('`estado` in (0,1)', name='CONSTRAINT_1'),
    # sa.PrimaryKeyConstraint('id'),
    # mysql_default_charset='utf8mb4',
    # mysql_engine='InnoDB'
    # )
    # op.create_table('usuarios',
    # sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    # sa.Column('nombres', mysql.VARCHAR(length=60), nullable=False),
    # sa.Column('fk_rol', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    # sa.Column('apellido_paterno', mysql.VARCHAR(length=30), nullable=False),
    # sa.Column('apellido_materno', mysql.VARCHAR(length=30), nullable=False),
    # sa.Column('correo', mysql.VARCHAR(length=60), nullable=True),
    # sa.Column('contraseña', mysql.VARCHAR(length=60), nullable=False),
    # sa.Column('telefono', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    # sa.Column('fecha_creacion', mysql.DATETIME(), nullable=True),
    # sa.Column('estado', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    # sa.CheckConstraint('`estado` in (0,1)', name='CONSTRAINT_1'),
    # sa.ForeignKeyConstraint(['fk_rol'], ['roles_aplicacion.id'], name='usuarios_ibfk_1'),
    # sa.PrimaryKeyConstraint('id'),
    # mysql_default_charset='utf8mb4',
    # mysql_engine='InnoDB'
    # )
    # op.create_index('correo', 'usuarios', ['correo'], unique=True)
    # op.drop_table('user_roles')
    # op.drop_table('users')
    # op.drop_table('roles')
    # ### end Alembic commands ###