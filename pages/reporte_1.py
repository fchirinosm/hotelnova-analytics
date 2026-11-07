from common import *

st.title('HotelNova | Reporte 1')
st.subheader('Demanda y cancelaciones')
st.caption('¿Cómo evoluciona la demanda y dónde se concentran las cancelaciones?')
st.caption('Ingeniería de Datos · Python + Streamlit + Plotly · Datos exportados de HotelNova · Periodo 2015–2017')
try:
    datos=aplicar_filtros(cargar_datos())
except Exception as error:
    st.error('No se pudo cargar el archivo de datos publicado. Comprueba que exista data/reservas_dashboard.csv.gz.')
    st.exception(error)
    st.stop()

total=len(datos)
cancelaciones=int(datos['is_canceled'].fillna(0).sum())
no_canceladas=total-cancelaciones
m1,m2,m3,m4=st.columns(4)
m1.metric('Reservas registradas',f'{total:,}')
m2.metric('Cancelaciones',f'{cancelaciones:,}')
m3.metric('Tasa de cancelación',f'{cancelaciones/total:.1%}')
m4.metric('Reservas no canceladas',f'{no_canceladas:,}')
st.caption('Se cuenta cada registro como una reserva. Las fechas corresponden a la llegada, no a la creación de la reserva.')
mensual=(datos.dropna(subset=['periodo']).groupby('periodo',as_index=False)
         .agg(reservas=('id_reserva','size'), cancelaciones=('is_canceled','sum')))
mensual['tasa_cancelacion']=(mensual['cancelaciones']/mensual['reservas']*100).round(2)
fig=px.line(mensual,x='periodo',y='reservas',markers=True,
            title='Evolución mensual de reservas',color_discrete_sequence=[AZUL],
            labels={'periodo':'Mes de llegada','reservas':'Reservas'})
barra(fig)
izq,der=st.columns(2)
with izq:
    fig=px.bar(mensual,x='periodo',y='cancelaciones',title='Cancelaciones por mes',
               color_discrete_sequence=[ROJO],labels={'periodo':'Mes de llegada','cancelaciones':'Cancelaciones'})
    barra(fig)
with der:
    por_hotel=resumen(datos,'hotel')
    fig=px.bar(por_hotel,x='hotel',y='tasa_cancelacion',title='Tasa de cancelación por hotel',
               color_discrete_sequence=[VERDE],text_auto='.1f',
               labels={'hotel':'Hotel','tasa_cancelacion':'Tasa de cancelación (%)'})
    fig.update_yaxes(range=[0, max(50, min(100, float(por_hotel['tasa_cancelacion'].max()) * 1.15))])
    barra(fig)
comparacion=por_hotel.copy()
comparacion['No canceladas']=comparacion['reservas']-comparacion['cancelaciones']
comparacion=comparacion.rename(columns={'cancelaciones':'Canceladas'})
comparacion_larga=comparacion.melt(id_vars='hotel',value_vars=['No canceladas','Canceladas'],var_name='Estado',value_name='Reservas')
fig=px.bar(comparacion_larga,x='hotel',y='Reservas',color='Estado',barmode='group',
           color_discrete_map={'No canceladas':VERDE,'Canceladas':ROJO},
           labels={'hotel':'Hotel'},title='Volumen de reservas por hotel y estado')
barra(fig)
peor=por_hotel.sort_values('tasa_cancelacion',ascending=False).iloc[0]
st.info(f"**Lectura de resultados:** {peor['hotel']} registra la mayor tasa de cancelación del periodo filtrado ({peor['tasa_cancelacion']:.1f}%). Compara también el volumen de reservas antes de priorizar acciones.")
st.caption('Cobertura parcial: 2015 comienza en julio y 2017 termina en agosto. No comparar totales anuales sin ajustar por meses disponibles.')
tabla(mensual.sort_values('periodo',ascending=False).round(2),'Detalle mensual de demanda')

st.divider()
st.caption('HotelNova · Proyecto académico · Fuente: Hotel Booking Demand (CSV histórico); versión web sin conexión en vivo. Datos 2015–2017.')
