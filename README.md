# TC_Embrapa

TC_Embrapa é uma API que coleta dados do site da Embrapa e permite que os usuários visualizem esses dados em diversos tipos de gráficos.

## Descrição

TC_Embrapa é uma API desenvolvida com FastAPI que oferece endpoints para autenticação de usuários, registro e visualização de dados obtidos do site da Embrapa. Os dados podem ser visualizados em diferentes formatos de gráficos, facilitando a análise e interpretação das informações.

## Contribuidores

- Jorge Kayodê Lima Trindade
- Octávio Ruiz Thomas

## Instalação

### Pré-requisitos

- Python 3.12 ou superior
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
    cd App_Embrapa
    pip install -r requirements.txt
    ```

4. Configure o banco de dados (caso o projeto não tenha o arquivo "database/clientes_database.db"):
    1. Execute o arquivo "utils/make.py" ele gerará o "clientes_database.db".

5. Baixe os dados da Embrapa:
    1. Baixe o [TrabalhoFiap - Feedback.ipynb](https://raw.githubusercontent.com/RedCanister/TC_Embrapa/master/Data_Embrapa/Dados_Embrapa/TrabalhoFiap%20-%20Feedback.ipynb) e execute-o para baixar os arquivos de dados.
    2. Após o download, mova os arquivos para o diretório `TC_Embrapa/Data_Embrapa/Dados_Embrapa/JSON`.

6. Inicie a aplicação:
    ```bash
    uvicorn main:app --reload
    ```

7. Em caso de problemas durante o processo de login que resultem em um erro relacionado ao módulo JWT, você pode executar o seguinte código para garantir que a instalação do JWT esteja correta:
    ```bash
    pip install --upgrade --force-reinstall PyJWT
    ```

## Uso

## Endpoints principais

- `GET /`: Redireciona para a página de login.
- `GET /page`: Retorna a página de login.
- `GET /cadastro`: Retorna a página de cadastro.
- `POST /register`: Registra um novo usuário.
- `POST /login`: Realiza login de usuário.
- `GET /producao`: Visualiza dados de produção.
- `GET /processamento`: Visualiza dados de processamento.
- `GET /comercializacao`: Visualiza dados de comercialização.
- `GET /importacao`: Visualiza dados de importação.
- `GET /exportacao`: Visualiza dados de exportação.

## Funcionalidades

- Autenticação de usuário com JWT.
- Registro de novos usuários.
- Login de usuários registrados.
- Visualização de dados extraídos do site da Embrapa em diferentes formatos de gráficos.
