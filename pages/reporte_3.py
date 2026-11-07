from common import *

st.title('HotelNova | Reporte 3')
st.subheader('Canales, segmentos y clientes')
st.caption('¿Qué canales y segmentos concentran las reservas y las cancelaciones?')
st.caption('Ingeniería de Datos · Python + Streamlit + Plotly · Datos exportados de HotelNova · Periodo 2015–2017')
try:
    datos=aplicar_filtros(cargar_datos())
except Exception as error:
    st.error('No se pudo cargar el archivo de datos publicado. Comprueba que exista data/reservas_dashboard.csv.gz.')
    st.exception(error)
    st.stop()

n=len(datos)
canales=resumen(datos,'canal')
segmentos=resumen(datos,'segmento')
clientes=resumen(datos,'tipo_cliente')
a,b,c,d=st.columns(4)
a.metric('Reservas',f'{n:,}')
b.metric('Canales identificados',f'{len(canales):,}')
c.metric('Segmentos identificados',f'{len(segmentos):,}')
d.metric('Tipos de cliente',f'{len(clientes):,}')
izq,der=st.columns(2)
with izq:
    fig=px.bar(canales.sort_values('reservas'),x='reservas',y='canal',orientation='h',title='Reservas por canal de distribución',
               color_discrete_sequence=[AZUL],
               labels={'canal':'Canal','reservas':'Reservas'})
    barra(fig)
    fig=px.bar(canales.sort_values('tasa_cancelacion'),x='tasa_cancelacion',y='canal',orientation='h',
               custom_data=['reservas','cancelaciones'],
               title='Tasa de cancelación por canal (%)',color_discrete_sequence=[ROJO],
               labels={'canal':'Canal','tasa_cancelacion':'Tasa de cancelación (%)'})
    fig.update_traces(hovertemplate='%{y}: %{x:.2f}% de cancelación<br>Reservas: %{customdata[0]:,}<br>Cancelaciones: %{customdata[1]:,}<extra></extra>',
                      text=canales.sort_values('tasa_cancelacion')['reservas'].map(lambda n: f'n={n:,}'),textposition='outside')
    fig.update_xaxes(range=[0,110])
    barra(fig)
with der:
    fig=px.bar(segmentos.sort_values('reservas'),x='reservas',y='segmento',orientation='h',title='Reservas por segmento de mercado',
               color_discrete_sequence=[VERDE],
               labels={'segmento':'Segmento','reservas':'Reservas'})
    barra(fig)
    fig=px.pie(clientes,names='tipo_cliente',values='reservas',hole=.55,
               title='Distribución por tipo de cliente')
    fig.update_traces(textinfo='percent',texttemplate='%{percent:.1%}',hovertemplate='%{label}: %{value:,} reservas (%{percent})<extra></extra>')
    barra(fig)
principal=canales.iloc[0]
st.info(f"**Lectura de resultados:** {principal['canal']} es el canal con más reservas ({principal['reservas']:,}, {principal['reservas']/n:.1%} del total filtrado). Evalúa su tasa de cancelación antes de recomendar aumentar su participación.")
grupo = segmentos[segmentos['segmento'].eq('Groups')]
if not grupo.empty:
    g = grupo.iloc[0]
    st.info(f"**Segmento Groups:** {g['reservas']:,} reservas y {g['tasa_cancelacion']:.2f}% de cancelación. Conviene examinar este segmento por su volumen y tasa de cancelación.")
st.caption('Precaución: Undefined registra 4 cancelaciones entre solo 5 reservas (80%). Ese tamaño de muestra es demasiado pequeño para concluir que sea el canal más problemático. Las tasas deben interpretarse junto con los volúmenes.')
tabla(canales,'Detalle por canal')
tabla(segmentos,'Detalle por segmento')
tabla(clientes,'Detalle por tipo de cliente')

st.divider()
st.caption('HotelNova · Proyecto académico · Fuente: Hotel Booking Demand (CSV histórico); versión web sin conexión en vivo. Datos 2015–2017.')
