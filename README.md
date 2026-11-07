# HotelNova Analytics — aplicación web

Tres dashboards interactivos para el proyecto de Ingeniería de Datos.

## Datos y alcance

La versión incluida usa `data/reservas_dashboard.csv.gz`, derivado del CSV histórico `hotel_bookings(1).csv` proporcionado para el proyecto. **No realiza consultas SQL Server en vivo**. La versión original de escritorio sí usa la base normalizada HotelNova. El paquete contiene también `exportar_desde_sqlserver.py` para reemplazar los datos publicados por una exportación exacta de la consulta SQL de los reportes originales.

## Probar localmente

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Publicar en Streamlit Community Cloud

1. Crea un repositorio de GitHub, por ejemplo `hotelnova-analytics`.
2. Sube el **contenido** de esta carpeta, incluyendo `data/reservas_dashboard.csv.gz`, `pages/`, `common.py`, `requirements.txt` y `streamlit_app.py`.
3. En https://share.streamlit.io/ pulsa **Create app** y selecciona el repositorio, rama `main` y archivo principal `streamlit_app.py`.
4. Pulsa **Deploy**. Verifica que los tres reportes funcionen con filtros y descargas CSV.
5. Comparte el enlace `https://<nombre>.streamlit.app` en el informe o presentación.

## Reemplazar el CSV por una exportación desde SQL Server

En el PC donde se encuentra HotelNova y con el entorno Python original (`pyodbc` instalado):

```powershell
python exportar_desde_sqlserver.py
```

El script consulta las mismas tablas y columnas usadas en los reportes SQL Server originales y sobrescribe `data/reservas_dashboard.csv.gz`. Comprueba los resultados, sube el nuevo archivo a GitHub y Streamlit actualizará la app.

## Advertencias

- El CSV de reservas es un conjunto de datos histórico público de ejemplo. Revisa las políticas del curso antes de publicarlo en un repositorio público.
- No subas credenciales, contraseñas, ni cadenas de conexión privadas.
- En la versión web, la opción de actualización en vivo desde SQL Server se sustituye por la lectura del archivo publicado.
- Los filtros y las tablas descargables se mantienen en cada dashboard.
