import pandas as pd
import plotly.express as px
import seaborn as sns 
import matplotlib.pyplot as plt
import locale
import dash
from dash import html,dcc
import plotly.graph_objects as go
#lectura del informe.csv

#definir el idioma
#locale.setlocale(locale.LC_TIME, 'es_Es')
Dventas = pd.read_csv("Datos_Ventas_Tienda.csv")
#convetir la columna fecha de un tipo de datos datetime
Dventas['Fecha'] = pd.to_datetime(Dventas['Fecha'],dayfirst=False)
#Traducciones
meses = {
     'January':'Enero',
     'February':'Febrero',
     'March':'Marzo',
     'April':'Abril',
     'May':'Mayo',
     'June':'Junio',
     'July':'Julio',
     'August':'Agosto',
     'September':'Septiembre',
     'October':'Octubre',
     'November':'Noviembre',
     'December':'Diciembre'
}
dias = {
    'Monday':'Lunes',
    'Tuesday':'Martes',
    'Wednesday':'Miercoles',
    'Thursday':'Jueves',
    'Friday':'Viernes',
    'Saturday':'Sabado',
    'Sunday':'Domingo'
}
morden = {
    'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
    'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
    'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
}
#crear una nueva columna dia,mes,año
Dventas['Mes'] = Dventas['Fecha'].dt.month_name().map(meses)
#para ordeneas los meses de forma cronologica
Dventas['numes'] = Dventas['Fecha'].dt.month
Dventas['Dia semana'] = Dventas['Fecha'].dt.day_name().map(dias)
Dventas['Año'] = Dventas['Fecha'].dt.to_period('M').astype(str)
#print(Dventas)
#crear filttro de venta mensuales
Vmensual = Dventas.groupby(['numes','Mes'])['Total Venta'].sum().reset_index()
#ordenar
Vmensual = Vmensual.sort_values('numes')
#crear el grafico
ventasmensual =px.line(Vmensual, x='Mes', y='Total Venta',markers=True,title='Ventas totales por mes')
#mostrar grafico
#ventasmensual.show(renderer = 'browser')
#filtro ventas x producto
Vproducto = Dventas.groupby('Producto')['Total Venta'].sum().reset_index()
#crear grafico de venta productos
Ventaspro = px.bar(Vproducto, x='Producto', y='Total Venta',color='Producto',title='Vental Totales por producto')
#Ventaspro.show(renderer = 'browser')
#filtro de producto x mes

Ventas = Dventas.groupby(['Producto','Mes'])['Total Venta'].sum().unstack().fillna(0)
#ordenar las columnas de acuerdo al mes
orden = sorted(Ventas.columns, key=lambda Mes:morden[Mes])
Ventas = Ventas[orden]
Ventaspm = go.Figure(data=go.Heatmap(
      z= Ventas.values,
      x = Ventas.columns,
      y = Ventas.index,
      colorscale="YlGnBu",
      hoverongaps=False
))

#Crear la app dashboard
app = dash.Dash(__name__)
#desplegar en render
server = app.server
#crear el tablero
app.layout = html.Div([
    html.H1("TABLERO DE VENTAS TIENDA 2025", style={"textAlign":"center"}),
    
    html.Div([
        dcc.Graph(figure=ventasmensual)
    ]),
    html.Div([
        dcc.Graph(figure=Ventaspro)
    ]),
    html.Div([
        html.H3("VENTAS DE PRODUCTO POR MES"),
        #Guardar como imagen
        dcc.Graph(figure=Ventaspm)
    ])
])


#ejecutar app
if __name__== "__main__":
    app.run(debug=True)