# HotelNova | Ingeniería de Datos 2026-II
# Datos locales exportados para despliegue web
import calendar
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

AZUL = '#245B82'
VERDE = '#169C91'
ROJO = '#D66762'
MESES_ES = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
MESES = {name.lower(): i for i, name in enumerate(calendar.month_name) if name}
MESES.update({'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,'agosto':8,'septiembre':9,'setiembre':9,'octubre':10,'noviembre':11,'diciembre':12})

@st.cache_data(show_spinner='Cargando datos históricos de HotelNova...')
def cargar_datos():
    ruta = Path(__file__).resolve().parent / 'data' / 'reservas_dashboard.csv.gz'
    df = pd.read_csv(ruta, compression='gzip')
    for col in ['is_canceled', 'arrival_date_year', 'adr', 'lead_time',
                'stays_in_weekend_nights', 'stays_in_week_nights']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['mes_num'] = df['arrival_date_month'].astype(str).str.strip().str.lower().map(MESES)
    df['periodo'] = pd.to_datetime(dict(year=df['arrival_date_year'],
                                         month=df['mes_num'], day=1), errors='coerce')
    df['noches'] = df['stays_in_weekend_nights'].fillna(0) + df['stays_in_week_nights'].fillna(0)
    df['valor_estimado'] = df['adr'] * df['noches']
    for col in ['hotel', 'canal', 'segmento', 'tipo_cliente']:
        df[col] = df[col].fillna('Sin especificar')
    return df

def aplicar_filtros(df):
    with st.sidebar:
        st.header('Filtros del reporte')
        anios = sorted(df['arrival_date_year'].dropna().astype(int).unique().tolist())
        sel_anios = st.multiselect('Año de llegada', anios, default=anios)
        hoteles = sorted(df['hotel'].unique().tolist())
        sel_hoteles = st.multiselect('Hotel', hoteles, default=hoteles)
        st.caption('Los filtros afectan todos los indicadores y gráficos de este reporte.')
        st.caption('Datos históricos publicados · versión sin conexión en vivo a SQL Server')
    resultado = df[df['arrival_date_year'].isin(sel_anios) & df['hotel'].isin(sel_hoteles)].copy()
    if resultado.empty:
        st.warning('No hay datos para los filtros seleccionados.')
        st.stop()
    return resultado

def barra(fig):
    fig.update_layout(template='plotly_white', margin=dict(l=20,r=20,t=65,b=25),
                      font=dict(family='Arial', size=12), hovermode='closest')
    st.plotly_chart(fig, use_container_width=True)

def tabla(df, nombre):
    st.markdown('**' + nombre + '**')
    visible = df.copy()
    if 'periodo' in visible.columns:
        fechas = pd.to_datetime(visible['periodo'])
        visible['periodo'] = fechas.map(lambda f: f'{MESES_ES[f.month-1]} {f.year}' if pd.notna(f) else 'Sin fecha')
    nombres = {'periodo':'Mes de llegada', 'reservas':'Reservas',
               'cancelaciones':'Cancelaciones', 'tasa_cancelacion':'Tasa de cancelación (%)',
               'adr_promedio':'ADR promedio', 'noches':'Noches reservadas',
               'valor_estimado':'Valor estimado', 'canal':'Canal',
               'segmento':'Segmento de mercado', 'tipo_cliente':'Tipo de cliente'}
    visible = visible.rename(columns=nombres)
    formatos = {c: st.column_config.NumberColumn(c, format='%,d')
                for c in ['Reservas','Cancelaciones','Noches reservadas'] if c in visible.columns}
    formatos.update({c: st.column_config.NumberColumn(c, format='%.2f')
                     for c in ['Tasa de cancelación (%)','ADR promedio']
                     if c in visible.columns})
    if 'Valor estimado' in visible.columns:
        visible['Valor estimado'] = visible['Valor estimado'].map(lambda x: f'{x:,.2f}' if pd.notna(x) else '')
    st.dataframe(visible, use_container_width=True, hide_index=True, column_config=formatos)
    st.download_button('Descargar tabla CSV', visible.to_csv(index=False).encode('utf-8-sig'),
                       file_name=nombre.lower().replace(' ', '_') + '.csv', mime='text/csv')

def resumen(df, col):
    t = (df.groupby(col, dropna=False, as_index=False)
         .agg(reservas=('id_reserva','size'), cancelaciones=('is_canceled','sum')))
    t['tasa_cancelacion'] = (t['cancelaciones'] / t['reservas'] * 100).round(2)
    return t.sort_values('reservas', ascending=False)

