from sqlalchemy import text  # Importa a função text do módulo sqlalchemy
from utils.make import engine  # Importa o objeto engine do módulo utils.make

# Classe para operações de consulta no banco de dados
class Queries:

    def __init__(self):
        pass  # O método init não faz nada neste caso

    @staticmethod
    def insert(email, password):
        """Método para inserir um novo registro na tabela clientes."""
        # Cria a query SQL para inserção de dados na tabela
        query = text('INSERT INTO clientes (email, password) VALUES (:email, :password)')
        # Conecta ao banco de dados e executa a query
        with engine.connect() as conn:
            conn.execute(query, {'email': email, 'password': password})  # Executa a query
            conn.commit()  # Confirma a transação

        # Realiza uma consulta para obter o registro recém-inserido
        query_user = text('SELECT email FROM clientes WHERE email=:email')
        with engine.connect() as conn:
            result = conn.execute(query_user, {'email': email})  # Executa a consulta
            user = result.fetchone()  # Obtém o primeiro registro retornado

        return user  # Retorna o registro inserido

    @staticmethod
    def checks(email):
        """Método para verificar se um e-mail está registrado na tabela 'clientes'."""
        # Cria a query SQL para verificar se um e-mail existe na tabela
        query = text('SELECT * FROM clientes WHERE email=:email')
        with engine.connect() as conn:
            result = conn.execute(query, {'email': email})  # Executa a consulta
            rows = result.fetchall()  # Obtém todos os registros retornados
            return len(rows) > 0  # Retorna True se o e-mail existir, False caso contrário

    @staticmethod
    def check_login(email):
        """Método para obter a senha criptografada de um usuário."""
        # Cria a query SQL para obter a senha de um usuário específico
        query = text('SELECT password FROM clientes WHERE email=:email')
        with engine.connect() as conn:
            result = conn.execute(query, {'email': email})  # Executa a consulta
            user = result.fetchone()  # Obtém o primeiro registro retornado
            return user  # Retorna a senha do usuário