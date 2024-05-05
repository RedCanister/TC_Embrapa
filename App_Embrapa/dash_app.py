import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from vini_rest.models import plotData

json_data = plotData.objects.all()
dfs = []
for item in json_data:
    df = pd.DataFrame(item.json_data)
    dfs.append(df)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Painel de dados de uva, vinho e derivados"),

    html.Label("Ano:"),
    dcc.Dropdown(
        id = 'ano-dropdown',
        options = [
            {'label': str(year), 'value': year} for df in dfs for year in df['year'].unique()
        ],
        multi = True,
        value = [],
        placeholder = "Selecione o ano"
    ),

    html.Label("Categoria:"),
    dcc.Dropdown(
        id = 'categoria-dropdown',
        options = [
            {'label': str(category), 'value': category} for df in dfs for category in df['category'].unique()
        ],
        multi = True,
        value = [],
        placeholder = 'Selecione a categoria'
    ),

    dcc.Graph(id = 'Dash_Embrapa')
])

@app.callback(
    Output('Dash_Embrapa', 'figure'),
    [Input('ano-dropdown', 'value'),
     Input('category-dropdown', 'value')]
)
def update_graph(selected_years, selected_categories):
    filtered_dfs = []
    for df in dfs:
        if not selected_years or set(selected_years).intersection(df['year'].unique()):
            if not selected_categories or set(selected_categories).intersection(df['category'].unique()):
                filtered_dfs.append(df)
    
    combined_df = pd.concat(filtered_dfs)


    return figure

if __name__ == '__main__':
    app.run_server(debug=True)