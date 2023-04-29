from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import numpy as np
import pandas as pd

df=pd.read_csv('https://raw.githubusercontent.com/lromeror/Luis_Romero/main/dataESPOL.csv')
dic_ubi={
    '9M':[-2.14662, -79.96666],
    '3H':[-2.1523, -79.95582],
    'GEA':[-2.14016, -79.96282],
    '13B':[-2.14558, -79.96507],
    '7B':[-2.14704, -79.96609] ,
    '11A':[-2.14478, -79.96772],
    '8F':[-2.14878, -79.96752],
    '8E':[-2.14873, -79.96782],
    '9F':[-2.14715, -79.96778],
    '11C':[-2.14563, -79.96683],
    '11D':[-2.14544, -79.96601],
    '3K':[-2.15122, -79.95424], 
}
def converEntero(df,fea):
    con=[]
    for s in df[fea]:
        s=s.split(',')
        con.append(int(s[0]))
    df[fea]=con

for w in ['PARALELO','CAPACIDAD']:
    converEntero(df,w)

tipo=[]
for j in list(df['PARALELO']):
    if j <= 5:
        tipo.append('Teórico')
    else:
        tipo.append('Práctico')

df['CLASE']=tipo
df['BLOQUE']=[(i.strip())for i in df['BLOQUE']]
df['lat']=[(dic_ubi[bl][0])for bl in list(df['BLOQUE'])]
df['lon']=[(dic_ubi[bl][1])for bl in list(df['BLOQUE'])]

dffil = df[['UNIDAD','NOMBRE','BLOQUE','CAPACIDAD','CLASE','lat','lon']].groupby(['UNIDAD','NOMBRE', 'BLOQUE','CAPACIDAD','CLASE','lat','lon'], as_index= False).count()

def normalizar_lat(df,bloque,lat):
    modiCor=[]
    compa=[]
    cont=0
    for bloque,lo in zip (df[bloque],df[lat]):
        if bloque not in compa:
            compa.append(bloque)
            modiCor.append(lo)
        else:
            cont=cont+0.0000009
            modiCor.append(lo-cont)
    
    df[lat+'2']=modiCor

def normalizar_lon(df,bloque,lon):
    modiCor=[]
    compa=[]
    cont=0
    for bloque,lo in zip (df[bloque],df[lon]):
        if bloque not in compa:
            compa.append(bloque)
            modiCor.append(lo)
        else:
            cont=cont+0.000009
            modiCor.append(lo-cont)
    
    df[lon+'2']=modiCor

normalizar_lon(dffil,'BLOQUE','lon')
normalizar_lat(dffil,'BLOQUE','lat')
faculta=list(dffil['UNIDAD'].unique())
faculta.append('Mapa Espol PAE')

app = Dash(__name__)
app.layout=html.Div([
    html.Div(children='Mapa Espol' , style={'textAlign':'center'}),
    dcc.Dropdown(faculta,'Mapa Espol PAE',id='facul_drop'),
    dcc.Graph(id='Facultad')
])
def mapaEspol(df,lat,lon,zo):
    fig1 = px.scatter_mapbox(df, lat="lat2", lon="lon2", hover_data=["BLOQUE", "CAPACIDAD", 'CLASE'],
                            zoom=zo, height=600,color='NOMBRE',size='CAPACIDAD')
    fig1.update_layout(mapbox_style="open-street-map", mapbox=dict(
            center=dict(
                lat=lat,
                lon=lon
            ),))
    fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})  
    return fig1

@callback(
    Output('Facultad','figure'),
    Input('facul_drop','value')
)
def mapa(value):
    if value=='Mapa Espol PAE':
        fig1=mapaEspol(dffil,-2.14730,-79.9630,15)          
    elif value=='Facultad de Ingeniería en Electricidad y Computación':
        df_facul=dffil[dffil['UNIDAD']==value]
        fig1 = mapaEspol(df_facul,-2.14466,-79.96772,17.5)       
    elif  value=='Facultad de Ciencias Sociales y Humanísticas':
        df_facul=dffil[dffil['UNIDAD']==value]
        fig1 = mapaEspol(df_facul,-2.14873,-79.96782,17)    
    elif value=='Facultad de Ciencias Naturales y Matemáticas':
        df_facul=dffil[dffil['UNIDAD']==value]
        fig1 = mapaEspol(df_facul,-2.14662,-79.96666,18.3)  
    elif value=='Facultad de Ciencias de la Vida':
        df_facul=dffil[dffil['UNIDAD']==value]
        fig1 = mapaEspol(df_facul,-2.15122,-79.95424,17)
    elif value=='ESCUELA SUPERIOR POLITECNICA DEL LITORAL':
        df_facul=dffil[dffil['UNIDAD']==value]
        fig1 = mapaEspol(df_facul,-2.14589,-79.96530,17)
    return fig1

if __name__ == '__main__':
    app.run_server(debug=True)
    