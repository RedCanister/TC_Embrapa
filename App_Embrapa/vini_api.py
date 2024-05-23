from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import plotly.express as px
from plots import plotsData
from data_ingest import json_list

app = FastAPI()
app.moount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

for json in json_list[:3]:
    json = plotsData.melt_df(json)

for json in json_list[3:]:
    json = plotsData.melt_df(json)


@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    plot_html = "plot_html"
    return templates.TemplateResponse("base.html", {"request": request, "title": "Home", "plot_html": plot_html})

@app.get("/producao")
async def page_produ():
    return 'html'

@app.get("/processamento")
async def page_procs():
    return 'html'

@app.get("/comercializacao")
async def page_comrc():
    return 'html'

@app.get("/importacao")
async def page_impor():
    return 'html'

@app.get("/exportacao")
async def page_exprt():
    return 'html'