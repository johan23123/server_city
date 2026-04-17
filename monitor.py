import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta

st.set_page_config(page_title="City Monitor GPS", layout="wide")

# Refrescar cada 5 segundos para ver el movimiento
st_autorefresh(interval=5000, key="datarefresh")

st.title("🚚 Panel de Control - City Constructora")

# URL de tu servidor en Render
URL_RENDER = "https://server-city.onrender.com/posiciones_actuales"

try:
    response = requests.get(URL_RENDER)
    datos = response.json()
    
    if isinstance(datos, list) and len(datos) > 0:
        df = pd.DataFrame(datos)
        
        # AJUSTE DE HORA (De Servidor a Jujuy -3hs)
        df['hora_dt'] = pd.to_datetime(df['hora'], format='%H:%M:%S', errors='coerce')
        df['hora'] = (df['hora_dt'] - timedelta(hours=3)).dt.strftime('%H:%M:%S')
        
        m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=14)

        for _, row in df.iterrows():
            # Limpiamos el estado: Mayúsculas y sin espacios
            est = str(row['estado']).upper().strip()
            
            # Colores: IDA (Verde), VUELTA (Azul), OBRA (Naranja)
            if est == 'VUELTA':
                color_icono = 'blue'
            elif est == 'ENTREGA' or est == 'OBRA':
                color_icono = 'orange'
            else:
                color_icono = 'green' # Por defecto IDA
            
            folium.Marker(
                [row['lat'], row['lon']],
                popup=f"Chofer: {row['chofer']} | Estado: {est} | Hora: {row['hora']}",
                tooltip=f"{row['chofer']} ({est})",
                icon=folium.Icon(color=color_icono, icon='truck', prefix='fa')
            ).add_to(m)

        st_folium(m, width=1200, height=500, key="mapa_fijo")
        
        st.subheader("Planilla de Movimientos")
        st.table(df[['chofer', 'estado', 'hora']])
        
    else:
        st.info("📡 Esperando señal... El chofer debe iniciar el viaje en la App.")
except Exception as e:
    st.error("Conectando con el servidor de City...")
