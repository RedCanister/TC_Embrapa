from fastapi import FastAPI, HTTPException, Depends, status, Response, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import jwt
from utils.models import Queries  # Importa a classe Queries do módulo utils.models
from datetime import datetime, timedelta, timezone

# Configurações JWT
SECRET_KEY = "voce_escolhe"  # Chave secreta para codificar/descodificar tokens JWT
ALGORITHM = "HS256"  # Algoritmo de criptografia utilizado para os tokens JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tempo de expiração em minutos

app = FastAPI()  # Criação da aplicação FastAPI
templates = Jinja2Templates(directory="templates")  # Templates HTML para renderização
password_crypto = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Contexto para criptografia de senhas

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

class UserCreate(BaseModel):
    """Modelo de dados para criação de usuário."""
    email: EmailStr  # Campo de e-mail validado
    password: str  # Campo de senha

class User(BaseModel):
    """Modelo de dados para usuário."""
    email: EmailStr  # Campo de e-mail validado

@app.get("/")
async def root():
    """Endpoint raiz que redireciona para a página."""
    return RedirectResponse("/page")

@app.get("/page", response_class=HTMLResponse)
async def get_login_page(request: Request):
    """Endpoint para retornar a página de login."""
    return templates.TemplateResponse("pagina.html", {"request": request})

@app.post("/register")
async def register(user: UserCreate):
    """Endpoint para registrar um novo usuário."""
    hashed_password = get_password(user.password)  # Obtém a senha criptografada
    db_checks = Queries.checks(user.email)  # Verifica se o e-mail já está registrado
    if db_checks:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")  # Retorna erro se o e-mail já existe

    db_user = Queries.insert(user.email, hashed_password)  # Insere o novo usuário no banco de dados
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")  # Retorna erro se houver um problema no servidor
    return {"message": "User created successfully", "user": {"email": db_user[0]}}

@app.post("/login")
async def login(user: UserCreate, response: Response):
    """Endpoint para realizar login de usuário."""
    db_check_login = Queries.check_login(user.email)  # Verifica se o usuário está registrado
    if db_check_login and verify_password(user.password, db_check_login[0]):  # Verifica a senha
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)  # Cria o token de acesso JWT

        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)  # Define o cookie com o token de acesso
        return {"message": "Login successful"}  # Retorna mensagem de sucesso
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")  # Retorna erro se o login falhar

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

@app.get("/visualization")
async def visualization(current_user: User = Depends(get_current_user)):
    """Endpoint para visualização com autenticação."""
    return {"message": "Visualização"}  # Retorna mensagem de visualização