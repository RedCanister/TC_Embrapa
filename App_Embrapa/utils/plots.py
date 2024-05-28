import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class plotsData():
    # PRÉ-PROCESSAMENTO DE DADOS
    
    # Para uso com conjuntos de dados com 2 colunas categóricas no início
    def melt_df(df):

        vars = ['Produto', 'Categoria']
        df.columns = vars + list(df.columns[2:])

        df_check = df.columns[2:]
        df = df[~df[df_check].apply(lambda linha: (linha == 0).all(), axis = 1)]

        melted_df = df.reset_index().melt(id_vars = vars, var_name = 'Year', value_name = 'Value')
        
        melted_df = melted_df[~melted_df['Year'].str.contains('index', case=False, na=False)]

        return melted_df

    # Para uso com conjuntos de dados com 1 coluna categórica no início
    def combine_df(df: pd.DataFrame):

        df_check = df.columns[1:]
        df_ = df[~df[df_check].apply(lambda linha: (linha == 0).all(), axis = 1)]

        data_temp = df_
        data_temp.rename(columns = {'País': 'Pais'}, inplace = True)

        kilos_columns = [col for col in data_temp.columns if not col.endswith('.1')]
        money_columns = [col for col in data_temp.columns if col.endswith('.1') or col =='Pais']

        df_kilos = data_temp[kilos_columns]
        df_money = data_temp[money_columns]

        df_money.columns = [col.replace('.1', '') if col != 'Pais' else col for col in df_money.columns]

        df_kilos_melted = df_kilos.melt(id_vars = ['Pais'], var_name = 'Year', value_name = 'Kilos')
        df_money_melted = df_money.melt(id_vars = ['Pais'], var_name = 'Year', value_name = 'Money')

        df_combined = pd.merge(df_kilos_melted, df_money_melted, on = ['Pais', 'Year'])

        df_combined['Year'] = df_combined['Year'].astype(int)

        return df_combined

    # FORMATAÇÃO DE GRÁFICOS

    def format_plot(fig):
        fig.update_layout(
            autosize = True,
            showlegend = True,
            plot_bgcolor = 'rgba(40, 40, 40, 0.9)',  # Set background color to a darker shade of grey
            paper_bgcolor = 'rgba(40, 40, 40, 0.9)',
            legend = dict(
                orientation = "h",
                yanchor = "bottom",
                y = -1.0,  # Adjust this value as needed
                xanchor = "center",
                x = 0.5,
                title_text = 'Legend',  # Optional: add a title to the legend
                bgcolor = 'rgba(50, 50, 50, 0.9)',  # Set background color for legend
                bordercolor = 'rgba(0, 0, 0, 0.5)',  # Set border color for legend
                borderwidth = 1,  # Set border width for legend
                traceorder = "normal",  # Set trace order to normal
                itemsizing = 'trace',  # Minimizable legend
                itemclick = "toggleothers",
                valign = "bottom",
            ),
            height = 700,
            width = 1800,
            font=dict(
                color='rgb(220, 220, 220)'  # Set font color to a lighter shade of grey
            ),
        )

        fig.update_xaxes(
            gridcolor='rgba(80, 80, 80, 0.5)',
            gridwidth=1
        )

        fig.update_yaxes(
            gridcolor='rgba(80, 80, 80, 0.5)',
            gridwidth=1
        )

        return fig
    
    # VISUALIZAÇÃO DE DADOS

    def line(df: pd.DataFrame, ):

        fig = px.line(df, x = 'Year', y = 'Value', color = 'Produto', line_group = 'Produto', facet_col = 'Categoria')
        
        plot_html = plotsData.format_plot(fig).to_html(full_html = False, include_plotlyjs = 'cdn')

        return plot_html


    def bar(df: pd.DataFrame, ):

        fig = px.bar(df, x = 'Year', y = 'Value', color = 'Produto',)
        
        plot_html = plotsData.format_plot(fig).to_html(full_html = False, include_plotlyjs = 'cdn')

        return plot_html


    def scatter(df: pd.DataFrame, ):

        fig = px.scatter(df, x = 'Year', y = 'Value', color = 'Produto',)
        
        plot_html = plotsData.format_plot(fig).to_html(full_html = False, include_plotlyjs = 'cdn')
        
        return plot_html


    def bubble(df: pd.DataFrame, ):
                
        fig = px.scatter(df, x = 'Year', y = 'Value', color = 'Produto', size = 'Value',)
        
        plot_html = plotsData.format_plot(fig).to_html(full_html = False, include_plotlyjs = 'cdn')
        
        return plot_html


    def line_combined(df: pd.DataFrame):

        fig = px.scatter(df, x='Kilos', y='Money', color='Pais', title='Scatter Plot of Kilos vs Money by Country')

        fig.update_layout(barmode = 'overlay', showlegend = True)
        
        plot_html = plotsData.format_plot(fig).to_html(full_html = False, include_plotlyjs = 'cdn')
        
        return plot_html


    def scatter_combined(df: pd.DataFrame):
        fig_combined_scatter = px.scatter(df, x = 'Year', y = 'Kilos', color = 'Pais', symbol = 'Pais', 
                                        title = 'Scatter Plot of Kilos and Money Over Years', labels = {'y':'Kilos'})

        # Add Money data as another trace
        for pais in df['Pais'].unique():
            df_subset = df[df['Pais'] == pais]
            fig_combined_scatter.add_trace(
                go.Scatter(x = df_subset['Year'], y = df_subset['Money'], mode = 'lines+markers', 
                        name = f'Money - {pais}', yaxis = 'y2')
            )

        """
        # Update layout to add secondary y-axis
        fig_combined_scatter.update_layout(
            yaxis2 = dict(
                title = 'Money',
                overlaying = 'y',
                side = 'right'
            ),
            legend = dict(
                x = 0.5,
                y = 1.2,
                traceorder = 'normal',
                font = dict(
                    family = 'sans-serif',
                    size = 12,
                    color = 'black'
                ),
                bgcolor = 'LightSteelBlue',
                bordercolor = 'Black',
                borderwidth = 2
            ),
            margin = dict(l = 0, r = 50, b = 0, t = 50),
        )"""

        plot_html = plotsData.format_plot(fig_combined_scatter).to_html(full_html = False, include_plotlyjs = 'cdn')
        
        return plot_html

    def scatter_combined_3d(dataframe: pd.DataFrame):
        # 3D scatter plot for Kilos and Money over Years
        fig_3d_scatter = px.scatter_3d(dataframe, x = 'Year', y = 'Kilos', z = 'Money', color = 'Pais', 
                                    title = '3D Scatter Plot of Kilos and Money Over Years', height = 800)

        """
        # Update layout for better readability
        fig_3d_scatter.update_layout(
            width = 1000,
            height = 800,
            scene = dict(
                xaxis = dict(title = 'Year', tickmode = 'linear', tick0 = 1970, dtick = 1),
                yaxis = dict(title = 'Kilos'),
                zaxis = dict(title = 'Money'),
                camera = dict(
                    eye = dict(x = 1.25, y = 1.25, z = 1.25)
                )
            ),
            margin=dict(l = 0, r = 0, b = 0, t = 40)
        )"""

        # Customize marker size and color
        fig_3d_scatter.update_traces(
            marker=dict(size = 8, opacity = 0.8, line = dict(width = 1, color = 'DarkSlateGrey')),
            selector = dict(mode = 'markers')
        )

        plot_html = plotsData.format_plot(fig_3d_scatter).to_html(full_html = False, include_plotlyjs = 'cdn')
        
        
        return plot_html
    