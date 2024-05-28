import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'clientes_database.db')
DATABASE_URL = f"sqlite:///{os.path.abspath(db_path)}"

engine = create_engine(DATABASE_URL)

# Cria um objeto MetaData
metadata = MetaData()

# Define a tabela clientes
clientes = Table(
    'clientes', metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, unique=True),
    Column('password', String)
)

# Crie todas as tabelas no banco de dados
metadata.create_all(engine)