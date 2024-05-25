from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from data_ingest import json_list
from plots import plotsData
import uvicorn


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

data_list = []

for data in json_list[:3]:
    data_list.append(plotsData.melt_df(data))

for data in json_list[3:]:
    data_list.append(plotsData.combine_df(data))

# Páginas de registro e login
@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    plot_html = "plot_html"
    return templates.TemplateResponse("base.html", {"request": request, "title": "Home", "plot_html": plot_html})

# Páginas de visualização de dados

# Produção
@app.get("/producao", response_class=HTMLResponse)
async def page_produ(request: Request):
    prod_data = data_list[0]
    plot_html_1 = plotsData.line(prod_data)
    plot_html_2 = plotsData.bubble(prod_data)
    return templates.TemplateResponse(
            "base.html", 
            {
                "request": request, 
                "title": "Visualização dos dados de produção", 
                "plot_html_1": plot_html_1,
                "plot_html_2": plot_html_2,
            }
        )

# Processamento
@app.get("/processamento", response_class=HTMLResponse)
async def page_procs(request: Request):
    proc_data = data_list[1]
    plot_html_1 = plotsData.scatter(proc_data)
    plot_html_2 = plotsData.bubble(proc_data)
    return templates.TemplateResponse(
            "base.html", 
            {
                "request": request, 
                "title": "Visualização dos dados de processamento", 
                "plot_html_1": plot_html_1,
                "plot_html_2": plot_html_2,
            }
        )

# Comercialização
@app.get("/comercializacao", response_class=HTMLResponse)
async def page_comrc(request: Request):
    comr_data = data_list[2]
    plot_html_1 = plotsData.bar(comr_data)
    plot_html_2 = plotsData.bubble(comr_data)
    return templates.TemplateResponse(
            "base.html", 
            {
                "request": request, 
                "title": "Visualização dos dados de comercialização", 
                "plot_html_1": plot_html_1,
                "plot_html_2": plot_html_2,
            }
        )

# Importação
@app.get("/importacao", response_class=HTMLResponse)
async def page_impor(request: Request):
    impr_data = data_list[3]
    plot_html_1 = plotsData.line_combined(impr_data)
    plot_html_2 = plotsData.scatter_combined_3d(impr_data)
    return templates.TemplateResponse(
            "base.html", 
            {
                "request": request, 
                "title": "Visualização dos dados de importação", 
                "plot_html_1": plot_html_1,
                "plot_html_2": plot_html_2,
            }
        )

# Exportação
@app.get("/exportacao", response_class=HTMLResponse)
async def page_exprt(request: Request):
    expr_data = data_list[4]
    plot_html_1 = plotsData.line_combined(expr_data)
    plot_html_2 = plotsData.scatter_combined_3d(expr_data)
    return templates.TemplateResponse(
            "base.html", 
            {
                "request": request, 
                "title": "Visualização dos dados de exportação", 
                "plot_html_1": plot_html_1,
                "plot_html_2": plot_html_2,
            }
        )

if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port=8000)
    #print(json_list[0])