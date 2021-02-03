from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


print('listo?')


def upgrade():

	op.alter_column('roles_aplicacion', column_name='nombres', new_column_name='nombre')
	print('listo!')


if __name__ == '__main__':
	upgrade()