from alembic import op
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


print('listo?')


def columna():

	op.alter_column('roles_aplicacion', column_name='nombres', new_column_name='nombre')
	print('listo!')


if __name__ == '__main__':
	upgrade()