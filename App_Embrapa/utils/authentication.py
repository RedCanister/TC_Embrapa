from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request, status
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from utils.models import Queries

import jwt


# Configurações JWT
SECRET_KEY = "voce_escolhe"  # Chave secreta para codificar/descodificar tokens JWT
ALGORITHM = "HS256"  # Algoritmo de criptografia utilizado para os tokens JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tempo de expiração em minutos

class UserCreate(BaseModel):
    """Modelo de dados para criação de usuário."""
    email: EmailStr  # Campo de e-mail validado
    password: str  # Campo de senha

class User(BaseModel):
    """Modelo de dados para usuário."""
    email: EmailStr  # Campo de e-mail validado

# Contexto para criptografia de senhas
password_crypto = CryptContext(schemes=["bcrypt"], deprecated="auto")  

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Função para criar um token de acesso JWT."""
    # Copia os dados do usuário
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})  # Adiciona a data de expiração ao token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Codifica o token JWT
    return encoded_jwt

def get_password(password):
    """Função para obter a senha criptografada."""
    return password_crypto.hash(password)

def verify_password(password_json, password_bd):
    """Função para verificar se a senha corresponde à senha armazenada."""
    return password_crypto.verify(password_json, password_bd)

async def get_current_user(request: Request):
    """Função para obter o usuário atual."""
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = request.cookies.get("access_token")  # Obtém o token de acesso do cookie
    if token is None:
        raise credentials_exception  # Retorna erro se não houver token
    try:
        payload = jwt.decode(token.split()[1], SECRET_KEY, algorithms=[ALGORITHM])  # Decodifica o token JWT
        username: str = payload.get("sub")  # Obtém o nome de usuário do token
        if username is None:
            raise credentials_exception  # Retorna erro se não houver nome de usuário no token
    except jwt.ExpiredSignatureError:
        raise credentials_exception  # Retorna erro se o token estiver expirado
    except jwt.InvalidTokenError:
        raise credentials_exception  # Retorna erro se o token for inválido
    user = Queries.check_login(username)  # Verifica se o usuário está registrado
    if user is None:
        raise credentials_exception  # Retorna erro se o usuário não existir
    return user