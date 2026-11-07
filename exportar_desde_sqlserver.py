"""Ejecutar en Windows, donde SQL Server HotelNova está instalado."""
from pathlib import Path
import gzip
import pandas as pd
import pyodbc

SQL = """
    SELECT r.id_reserva, r.is_canceled, r.arrival_date_year, r.arrival_date_month,
           r.stays_in_weekend_nights, r.stays_in_week_nights, r.adr,
           r.lead_time, r.id_hotel, r.id_canal, r.id_segmento, r.id_tipo_cliente,
           h.nombre_hotel AS hotel,
           cd.descripcion_canal AS canal,
           sm.descripcion_segmento AS segmento,
           tc.descripcion_tipo_cliente AS tipo_cliente
    FROM dbo.RESERVA AS r
    INNER JOIN dbo.HOTEL AS h ON h.id_hotel = r.id_hotel
    LEFT JOIN dbo.CANAL_DISTRIBUCION AS cd ON cd.id_canal = r.id_canal
    LEFT JOIN dbo.SEGMENTO_MERCADO AS sm ON sm.id_segmento = r.id_segmento
    LEFT JOIN dbo.TIPO_CLIENTE AS tc ON tc.id_tipo_cliente = r.id_tipo_cliente
    """

CONEXION = ('DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=DESKTOP-UKI9H1A;DATABASE=HotelNova;'
            'Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes;')

with pyodbc.connect(CONEXION, timeout=15) as con:
    cursor = con.cursor()
    cursor.execute(SQL)
    nombres = [c[0] for c in cursor.description]
    filas = [tuple(f) for f in cursor.fetchall()]

resultado = pd.DataFrame.from_records(filas, columns=nombres)
ruta = Path(__file__).resolve().parent / 'data' / 'reservas_dashboard.csv.gz'
ruta.parent.mkdir(parents=True, exist_ok=True)
resultado.to_csv(ruta, index=False, compression='gzip')
print(f'Exportadas {len(resultado):,} reservas a {ruta}')
print('Hoteles:', resultado['hotel'].value_counts().to_dict())
