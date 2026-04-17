import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta

st.set_page_config(page_title="City Monitor Real-Time", layout="wide")

# CONFIGURACIÓN: Refrescar cada 5 segundos
st_autorefresh(interval=5000, key="datarefresh")

st.title("🚚 Seguimiento en Tiempo Real - City Constructora")

URL_RENDER = "https://server-city.onrender.com/posiciones_actuales"

try:
    response = requests.get(URL_RENDER)
    datos = response.json()
    
    if isinstance(datos, list) and len(datos) > 0:
        df = pd.DataFrame(datos)
        
        # --- ARREGLO DE HORA (Zona Horaria Argentina -3) ---
        # Convertimos la hora del servidor a formato tiempo y le restamos 3 horas
        df['hora_dt'] = pd.to_datetime(df['hora'], format='%H:%M:%S', errors='coerce')
        df['hora'] = (df['hora_dt'] - timedelta(hours=3)).dt.strftime('%H:%M:%S')
        
        # Calculamos el centro del mapa
        centro_lat = df['lat'].mean()
        centro_lon = df['lon'].mean()
        
        m = folium.Map(location=[centro_lat, centro_lon], zoom_start=14)

        for _, row in df.iterrows():
            # --- COLORES DINÁMICOS CORREGIDOS ---
            # Verde para IDA, Azul para VUELTA, Naranja para cualquier otro estado
            if row['estado'] == 'IDA':
                color_icono = 'green'
            elif row['estado'] == 'VUELTA':
                color_icono = 'blue'
            else:
                color_icono = 'orange'
            
            folium.Marker(
                [row['lat'], row['lon']],
                popup=f"Chofer: {row['chofer']} | Estado: {row['estado']} | Hora: {row['hora']}",
                tooltip=f"{row['chofer']} ({row['estado']})",
                icon=folium.Icon(color=color_icono, icon='truck', prefix='fa')
            ).add_to(m)

        # Mostramos el mapa
        st_folium(m, width=1200, height=500, key="mapa_fijo")
        
        st.write(f"✅ Última señal recibida (Hora Jujuy): {df['hora'].iloc[-1]}")
        
        # Mostrar tabla con la hora corregida
        st.subheader("Planilla de Movimientos")
        st.table(df[['chofer', 'estado', 'hora', 'lat', 'lon']])
        
    else:
        st.info("📡 Esperando señal... Asegurate de que el chofer tenga la App abierta y en 'RUTA'.")
        m_vacio = folium.Map(location=[-24.185, -65.300], zoom_start=13)
        st_folium(m_vacio, width=1200, height=500)

except Exception as e:
    st.error(f"Error de conexión: {e}")
