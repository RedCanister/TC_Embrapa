# TC_Embrapa

TC_Embrapa é uma API que coleta dados do site da Embrapa e permite que os usuários visualizem esses dados em diversos tipos de gráficos.

## Descrição

TC_Embrapa é uma API desenvolvida com FastAPI que oferece endpoints para autenticação de usuários, registro e visualização de dados obtidos do site da Embrapa. Os dados podem ser visualizados em diferentes formatos de gráficos, facilitando a análise e interpretação das informações.

## Contribuidores

- Jorge Kayodê Lima Trindade
- Octávio Ruiz Thomas

## Instalação

### Pré-requisitos

- Python 3.7 ou superior
- SQLite

### Passos para instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/RedCanister/TC_Embrapa.git
    cd tc_embrapa
    ```

2. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

    ```
    Para usuários do VSCode, é possível utilizar o atalho Ctrl + Shift + P para realizar a instalação rápido do ambiente virtual.
    Na barra de pesquise escreva:
    1. Python: Create Environment
    2. Venv
    3. A Versão mais recente do Python
    4. Selecione o requirements.txt 
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure o banco de dados:
    ```bash
    python -c "from utils.make import engine; from sqlalchemy import MetaData; metadata = MetaData(bind=engine); metadata.create_all()"
    ```

5. Baixe os dados da Embrapa:
    1. Baixe o [notebook.ipynb](link) e execute-o para baixar os arquivos de dados.
    2. Após o download, mova os arquivos para o diretório `TC_Embrapa/Data_Embrapa/Dados_Embrapa/JSON`.

6. Inicie a aplicação:
    ```bash
    uvicorn main:app --reload
    ```

## Uso

### Endpoints principais

#### Registro de Usuário

- **Endpoint**: `/register`
- **Método**: `POST`
- **Descrição**: Registra um novo usuário.

- **Exemplo de Request**:
    ```json
    {
        "email": "usuario@exemplo.com",
        "password": "senha_secreta"
    }
    ```

- **Exemplo de Response**:
    ```json
    {
        "message": "User created successfully",
        "user": {
            "email": "usuario@exemplo.com"
        }
    }
    ```

#### Login de Usuário

- **Endpoint**: `/login`
- **Método**: `POST`
- **Descrição**: Realiza login do usuário.

- **Exemplo de Request**:
    ```json
    {
        "email": "usuario@exemplo.com",
        "password": "senha_secreta"
    }
    ```

- **Exemplo de Response**:
    ```json
    {
        "message": "Login successful"
    }
    ```

#### Visualização de Dados

- **Endpoint**: `/visualization`
- **Método**: `GET`
- **Descrição**: Retorna a visualização dos dados (autenticação necessária).

- **Exemplo de Response**:
    ```json
    {
        "message": "Visualização"
    }
    ```

## Funcionalidades

- Autenticação de usuário com JWT.
- Registro de novos usuários.
- Login de usuários registrados.
- Visualização de dados extraídos do site da Embrapa em diferentes formatos de gráficos.

## Licença

Este projeto está licenciado sob a Licença MIT.
