from common import *

st.title('HotelNova | Reporte 2')
st.subheader('Tarifas y estadías')
st.caption('¿Cómo cambian la tarifa diaria, las noches reservadas y el valor estimado?')
st.caption('Ingeniería de Datos · Python + Streamlit + Plotly · Datos exportados de HotelNova · Periodo 2015–2017')
try:
    datos=aplicar_filtros(cargar_datos())
except Exception as error:
    st.error('No se pudo cargar el archivo de datos publicado. Comprueba que exista data/reservas_dashboard.csv.gz.')
    st.exception(error)
    st.stop()

todas_no_canceladas = datos[datos['is_canceled'] == 0].copy()
no_canceladas = todas_no_canceladas[
    todas_no_canceladas['adr'].notna() & (todas_no_canceladas['adr'] >= 0)
].copy()
excluidas_adr = len(todas_no_canceladas) - len(no_canceladas)
if no_canceladas.empty:
    st.warning('No hay reservas no canceladas con ADR válido.')
    st.stop()
noches=no_canceladas['noches'].sum()
valor=no_canceladas['valor_estimado'].sum()
a,b,c,d=st.columns(4)
a.metric('Reservas no canceladas',f'{len(todas_no_canceladas):,}')
b.metric('ADR promedio',f'{no_canceladas["adr"].mean():,.2f}')
c.metric('Estadía media',f'{no_canceladas["noches"].mean():.1f} noches')
d.metric('Valor estimado',f'{valor:,.2f}')
texto_exclusion = (f'Se excluye {excluidas_adr:,} reserva' if excluidas_adr == 1 else f'Se excluyen {excluidas_adr:,} reservas')
st.caption(f'Para los indicadores de tarifas se usan {len(no_canceladas):,} reservas con ADR válido (no negativo). {texto_exclusion} del cálculo de ADR y valor estimado; el total de reservas no canceladas se conserva.')
st.info('**Importante:** ADR y valor estimado se muestran en unidades monetarias del dataset, cuya moneda no está identificada aquí. Valor estimado = ADR × noches para reservas no canceladas; no equivale a ingresos cobrados.')
mensual=(no_canceladas.dropna(subset=['periodo']).groupby('periodo',as_index=False)
         .agg(adr_promedio=('adr','mean'),noches=('noches','sum'),
              valor_estimado=('valor_estimado','sum'),reservas=('id_reserva','size')))
fig=px.line(mensual,x='periodo',y='adr_promedio',markers=True,
            title='Evolución mensual del ADR (reservas no canceladas)',
            color_discrete_sequence=[AZUL],labels={'periodo':'Mes de llegada','adr_promedio':'ADR promedio'})
fig.update_traces(customdata=[[f'{MESES_ES[p.month-1]} {p.year}'] for p in mensual['periodo']],
                  hovertemplate='Mes: %{customdata[0]}<br>ADR promedio: %{y:,.2f}<extra></extra>')
barra(fig)
izq,der=st.columns(2)
with izq:
    # Valores extremos se muestran en tabla; rango acotado mejora la legibilidad.
    max_noches=int(no_canceladas['noches'].quantile(.99))
    hist=no_canceladas[no_canceladas['noches'].between(0,max_noches)].copy()
    fig=px.histogram(hist,x='noches',nbins=min(max_noches+1,20),
                     title=f'Duración de estadías (hasta percentil 99: {max_noches} noches)',
                     color_discrete_sequence=[VERDE],
                     labels={'noches':'Noches por reserva','count':'Cantidad de reservas'})
    fig.update_yaxes(title_text='Cantidad de reservas')
    fig.update_traces(hovertemplate='Noches por reserva: %{x}<extra></extra>')
    barra(fig)
with der:
    fig=px.bar(mensual,x='periodo',y='valor_estimado',
               title='Valor estimado mensual de reservas no canceladas',
               color_discrete_sequence=[AZUL],
               labels={'periodo':'Mes de llegada','valor_estimado':'ADR × noches'})
    fig.update_traces(customdata=[[f'{MESES_ES[p.month-1]} {p.year}'] for p in mensual['periodo']],
                      hovertemplate='Mes: %{customdata[0]}<br>Valor estimado: %{y:,.2f}<extra></extra>')
    barra(fig)
adr_hoteles=(no_canceladas.groupby('hotel',as_index=False)
             .agg(adr_promedio=('adr','mean'),reservas=('id_reserva','size')))
fig=px.bar(adr_hoteles,x='hotel',y='adr_promedio',color_discrete_sequence=[VERDE],
           title='ADR promedio por hotel (reservas no canceladas con ADR válido)',
           labels={'hotel':'Hotel','adr_promedio':'ADR promedio'},text_auto='.2f')
barra(fig)
if len(adr_hoteles)>=2:
    mayor=adr_hoteles.loc[adr_hoteles['adr_promedio'].idxmax()]
    menor=adr_hoteles.loc[adr_hoteles['adr_promedio'].idxmin()]
    st.info(f"**Comparación entre hoteles:** {mayor['hotel']} tiene un ADR promedio de {mayor['adr_promedio']:,.2f} frente a {menor['adr_promedio']:,.2f} de {menor['hotel']} (diferencia de {mayor['adr_promedio']-menor['adr_promedio']:,.2f}). Esta comparación utiliza los filtros seleccionados.")
max_adr=mensual.loc[mensual['adr_promedio'].idxmax()]
mes_maximo = f"{MESES_ES[max_adr['periodo'].month - 1]} {max_adr['periodo'].year}"
st.info(f"**Lectura de resultados:** el ADR promedio mensual más alto en los filtros seleccionados corresponde a {mes_maximo} ({max_adr['adr_promedio']:,.2f}). Una tarifa mayor no implica necesariamente mayores ingresos reales.")
st.caption('El histograma muestra hasta el percentil 99 de duración para facilitar la lectura. Las métricas y tablas incluyen todas las reservas con ADR válido.')
tabla(mensual.sort_values('periodo',ascending=False).round(2),'Detalle mensual de tarifas')

st.divider()
st.caption('HotelNova · Proyecto académico · Fuente: Hotel Booking Demand (CSV histórico); versión web sin conexión en vivo. Datos 2015–2017.')
