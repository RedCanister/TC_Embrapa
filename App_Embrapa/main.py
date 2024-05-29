from fastapi import FastAPI, Request, HTTPException, Depends, status, Response
from utils.authentication import (
    ACCESS_TOKEN_EXPIRE_MINUTES,  
    UserCreate, 
    User, 
    create_access_token, 
    get_current_user, 
    get_password, 
    verify_password,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from process.data_ingest import data_list
from utils.plots import plotsData
from utils.models import Queries
from datetime import timedelta

import uvicorn
import os


# Inicializando o aplicativo e carregando os arquivos
app = FastAPI()

cur_dir = os.path.dirname(os.path.abspath(__file__))

static_dir = os.path.join(cur_dir, "static")
templates_dir = os.path.join(cur_dir, "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)
    
# Páginas de registro e login

@app.get("/")
async def root():
    """Endpoint raiz que redireciona para a página."""
    return RedirectResponse("/page")

# Página de login
@app.get("/page", response_class=HTMLResponse)
async def get_login_page(request: Request):
    """Endpoint para retornar a página de login."""
    return templates.TemplateResponse("pagina.html", {"request": request})

# Página de cadastro do usuário
@app.get("/cadastro", response_class=HTMLResponse)
async def get_login_page(request: Request):
    """Endpoint para retornar a página de cadastro."""
    return templates.TemplateResponse("cadastro.html", {"request": request})

# Redirecionamento do usuário para o registro no banco de dados
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

# Redirecionamento para a validação do login do usuário
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

# Páginas de visualização de dados

# Produção
@app.get("/producao", response_class=HTMLResponse)
async def page_produ(request: Request, current_user: User = Depends(get_current_user)):
    prod_data = data_list[0]
    plot_html_1 = plotsData.line(prod_data)
    plot_html_2 = plotsData.bubble(prod_data)
    return templates.TemplateResponse(
            "base_plots.html", 
            {
                "request": request, 
                "title": "Visualização dos dados de produção", 
                "plot_html_1": plot_html_1,
                "plot_html_2": plot_html_2,
            }
        )

# Processamento
@app.get("/processamento", response_class=HTMLResponse)
async def page_procs(request: Request, current_user: User = Depends(get_current_user)):
    proc_data = data_list[1]
    plot_html_1 = plotsData.scatter(proc_data)
    plot_html_2 = plotsData.bubble(proc_data)
    return templates.TemplateResponse(
            "base_plots.html", 
            {
                "request": request, 
                "title": "Visualização dos dados de processamento", 
                "plot_html_1": plot_html_1,
                "plot_html_2": plot_html_2,
            }
        )

# Comercialização
@app.get("/comercializacao", response_class=HTMLResponse)
async def page_comrc(request: Request, current_user: User = Depends(get_current_user)):
    comr_data = data_list[2]
    plot_html_1 = plotsData.bar(comr_data)
    plot_html_2 = plotsData.bubble(comr_data)
    return templates.TemplateResponse(
            "base_plots.html", 
            {
                "request": request, 
                "title": "Visualização dos dados de comercialização", 
                "plot_html_1": plot_html_1,
                "plot_html_2": plot_html_2,
            }
        )

# Importação
@app.get("/importacao", response_class=HTMLResponse)
async def page_impor(request: Request, current_user: User = Depends(get_current_user)):
    impr_data = data_list[3]
    plot_html_1 = plotsData.line_combined(impr_data)
    plot_html_2 = plotsData.scatter_combined_3d(impr_data)
    return templates.TemplateResponse(
            "base_plots.html", 
            {
                "request": request, 
                "title": "Visualização dos dados de importação", 
                "plot_html_1": plot_html_1,
                "plot_html_2": plot_html_2,
            }
        )

# Exportação
@app.get("/exportacao", response_class=HTMLResponse)
async def page_exprt(request: Request, current_user: User = Depends(get_current_user)):
    expr_data = data_list[4]
    plot_html_1 = plotsData.line_combined(expr_data)
    plot_html_2 = plotsData.scatter_combined_3d(expr_data)
    return templates.TemplateResponse(
            "base_plots.html", 
            {
                "request": request, 
                "title": "Visualização dos dados de exportação", 
                "plot_html_1": plot_html_1,
                "plot_html_2": plot_html_2,
            }
        )

if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port=8000)
