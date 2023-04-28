#Importamos todas las librerias
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

#Cargamos la data
df=pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

#Instanciamos DASH
app=Dash(__name__)

#Layout
app.layout=html.Div(
    children=[html.Div(children='My First App with Data, Graph, and Controls',style={'textAlign':'center'}),
              
              
              
              ])


if __name__ == '__main__':
    app.run_server(debug=True)