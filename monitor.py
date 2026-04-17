import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="City Monitor Real-Time", layout="wide")

# CONFIGURACIÓN: Refrescar cada 5000 milisegundos (5 segundos)
st_autorefresh(interval=5000, key="datarefresh")

st.title("🚚 Seguimiento en Tiempo Real - City Constructora")

URL_RENDER = "https://server-city.onrender.com/posiciones_actuales"

try:
    response = requests.get(URL_RENDER)
    datos = response.json()
    
    if isinstance(datos, list) and len(datos) > 0:
        df = pd.DataFrame(datos)
        
        # Calculamos el centro del mapa basado en los camiones activos
        centro_lat = df['lat'].mean()
        centro_lon = df['lon'].mean()
        
        m = folium.Map(location=[centro_lat, centro_lon], zoom_start=14)

        for _, row in df.iterrows():
            # Color dinámico: Verde si está en ruta, Naranja si llegó a obra
            color_icono = 'green' if row['estado'] == 'IDA' else 'orange'
            
            folium.Marker(
                [row['lat'], row['lon']],
                popup=f"Chofer: {row['chofer']} | Hora: {row['hora']}",
                tooltip=row['chofer'],
                icon=folium.Icon(color=color_icono, icon='truck', prefix='fa')
            ).add_to(m)

        # Mostramos el mapa
        st_folium(m, width=1200, height=500, key="mapa_fijo")
        
        st.write(f"✅ Última actualización: {df['hora'].iloc[-1]}")
        st.table(df)
    else:
        st.info("📡 Esperando señal de los camiones... Asegurate de que el chofer haya puesto 'SALIR A RUTA'.")
        # Mostramos un mapa vacío de Jujuy mientras esperamos
        m_vacio = folium.Map(location=[-24.185, -65.300], zoom_start=13)
        st_folium(m_vacio, width=1200, height=500)

except Exception as e:
    st.error(f"Conectando con el servidor de City Constructora...")