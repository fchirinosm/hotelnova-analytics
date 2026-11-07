import streamlit as st

st.set_page_config(page_title='HotelNova Analytics', page_icon='🏨', layout='wide')

pg = st.navigation([
    st.Page('pages/reporte_1.py', title='Demanda y cancelaciones', icon='📈', default=True),
    st.Page('pages/reporte_2.py', title='Tarifas y estadías', icon='💰'),
    st.Page('pages/reporte_3.py', title='Canales, segmentos y clientes', icon='👥'),
])
st.sidebar.markdown('## 🏨 HotelNova Analytics')
st.sidebar.caption('Proyecto académico · Ingeniería de Datos')
st.sidebar.info('Versión web con datos históricos exportados. No consulta SQL Server en tiempo real.')
pg.run()
