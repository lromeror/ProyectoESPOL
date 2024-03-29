from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

app.layout = html.Div([
    #Esta es la forma sin especificar el parametro childrn
    html.H1(children='Title of Dash App hey ', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content'),
    html.H2(id='ProbandoDASh')
    ])




#intentamos relacionar lo que esta en el layout
#id en dash le da cierto indetificar ciertas cosas para despues relacionar

@callback(#Es un decorador
    Output('graph-content', 'figure'),
    Output('ProbandoDASh','children'),
    Input('dropdown-selection', 'value')#Deleccion del dropdown
)

def fuctionGraph(value):
    
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop'),value

if __name__ == '__main__':
    app.run_server(debug=True)
