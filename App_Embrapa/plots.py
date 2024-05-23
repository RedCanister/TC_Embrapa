import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class plotsData():
    """
    plot_bgcolor
    paper_bgcolor
    font_color
    """
    
    # Para uso com conjuntos de dados com 2 colunas categóricas no início
    def melt_df(dataframe, ids: list, var: str, value: str):

        df_check = dataframe.columns[2:]
        dataframe = dataframe[~dataframe[df_check].apply(lambda linha: (linha == 0).all(), axis = 1)]

        melted_df = dataframe.reset_index().melt(ids = ids, var_name = var, value_name = value)
        
        return melted_df


    def line(dataframe: pd.DataFrame, x: str, y: str, color: str, lines: str, facet: str):
        fig = px.line(dataframe, x = x, y = y, color = color, line_group = lines, facet_col = facet)
        
        plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        return plot_html


    def bar(dataframe: pd.DataFrame, x: str, y: str, color: str,):
        fig = px.bar(dataframe, x = x, y = y, color = color)
        
        plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        return plot_html


    def scatter(dataframe: pd.DataFrame, x: str, y: str, color: str,):
        fig = px.scatter(dataframe, x = x, y = y, color = color,)
        
        plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        return plot_html


    def bubble(dataframe: pd.DataFrame, x: str, y: str, color: str, size):
        fig = px.scatter(dataframe, x = x, y = y, size = size, color = color)
        
        plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        return plot_html


    def line(dataframe: pd.DataFrame, x: str, y: str, color: str, line: str, facet: str):
        fig = px.line(dataframe, x = x, y = y, color = color, line_group = line, facet_col = facet)
        
        plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        return plot_html

    # Para uso com conjuntos de dados com 1 coluna categórica no início
    def combine_df(dataframe: pd.DataFrame):

        df_check = dataframe.columns[1:]
        dataframe = dataframe[~dataframe[df_check].apply(lambda linha: (linha == 0).all(), axis = 1)]

        data_temp = dataframe
        data_temp.rename(columns={'País': 'Pais'}, inplace=True)

        kilos_columns = [col for col in data_temp.columns if not col.endswith('.1')]
        money_columns = [col for col in data_temp.columns if col.endswith('.1') or col =='Pais']

        df_kilos = data_temp[kilos_columns]
        df_money = data_temp[money_columns]

        df_money.columns = [col.replace('.1', '') if col != 'Pais' else col for col in df_money.columns]

        df_kilos_melted = df_kilos.melt(id_vars=['Pais'], var_name='Year', value_name='Kilos')
        df_money_melted = df_money.melt(id_vars=['Pais'], var_name='Year', value_name='Money')

        df_combined = pd.merge(df_kilos_melted, df_money_melted, on=['Pais', 'Year'])

        df_combined['Year'] = df_combined['Year'].astype(int)

        return df_combined

    def line_combined(dataframe: pd.DataFrame):
        fig_scatter = px.scatter(dataframe, x='Kilos', y='Money', color='Pais', 
                                title='Scatter Plot of Kilos vs Money')
        
        plot_html = fig_scatter.to_html(full_html=False, include_plotlyjs='cdn')
        return plot_html


    def scatter_combined(dataframe: pd.DataFrame):
        fig_combined_scatter = px.scatter(dataframe, x='Year', y='Kilos', color='Pais', symbol='Pais', 
                                        title='Scatter Plot of Kilos and Money Over Years', labels={'y':'Kilos'})

        # Add Money data as another trace
        for pais in dataframe['Pais'].unique():
            df_subset = dataframe[dataframe['Pais'] == pais]
            fig_combined_scatter.add_trace(
                go.Scatter(x=df_subset['Year'], y=df_subset['Money'], mode='lines+markers', 
                        name=f'Money - {pais}', yaxis='y2')
            )

        # Update layout to add secondary y-axis
        fig_combined_scatter.update_layout(
            yaxis2=dict(
                title='Money',
                overlaying='y',
                side='right'
            ),
            legend=dict(
                x=0.5,
                y=1.2,
                traceorder='normal',
                font=dict(
                    family='sans-serif',
                    size=12,
                    color='black'
                ),
                bgcolor='LightSteelBlue',
                bordercolor='Black',
                borderwidth=2
            ),
            margin=dict(l=0, r=50, b=0, t=50)
        )

        plot_html = fig_combined_scatter.to_html(full_html=False, include_plotlyjs='cdn')
        return plot_html

    def scatter_combined_3d(dataframe: pd.DataFrame):
        # 3D scatter plot for Kilos and Money over Years
        fig_3d_scatter = px.scatter_3d(dataframe, x='Year', y='Kilos', z='Money', color='Pais', 
                                    title='3D Scatter Plot of Kilos and Money Over Years')

        # Update layout for better readability
        fig_3d_scatter.update_layout(
            width=1000,
            height=800,
            scene=dict(
                xaxis=dict(title='Year', tickmode='linear', tick0=1970, dtick=1),
                yaxis=dict(title='Kilos'),
                zaxis=dict(title='Money'),
                camera=dict(
                    eye=dict(x=1.25, y=1.25, z=1.25)
                )
            ),
            margin=dict(l=0, r=0, b=0, t=40)
        )

        # Customize marker size and color
        fig_3d_scatter.update_traces(
            marker=dict(size=8, opacity=0.8, line=dict(width=1, color='DarkSlateGrey')),
            selector=dict(mode='markers')
        )

        plot_html = fig_3d_scatter.to_html(full_html=False, include_plotlyjs='cdn')
        return plot_html
    