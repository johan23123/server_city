from fastapi import FastAPI, Body
import sqlite3
from datetime import datetime

app = FastAPI()

# Función para conectar a la DB
def conectar_db():
    conn = sqlite3.connect('logistica_city.db')
    return conn

# Crear las tablas apenas arranca
@app.on_event("startup")
def startup():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS viajes 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, chofer TEXT, estado TEXT, inicio TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS posiciones 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, id_viaje INTEGER, lat REAL, lon REAL, hora TEXT, estado TEXT)''')
    conn.commit()
    conn.close()

@app.get("/")
def home():
    return {"status": "City Constructora Server Online"}

@app.get("/iniciar")
def iniciar_viaje(chofer: str):
    conn = conectar_db()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO viajes (chofer, estado, inicio) VALUES (?, 'IDA', ?)", (chofer, ahora))
    id_viaje = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id_viaje": id_viaje}

@app.post("/gps")
def recibir_gps(data: dict = Body(...)):
    conn = conectar_db()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%H:%M:%S")
    cursor.execute("INSERT INTO posiciones (id_viaje, lat, lon, hora, estado) VALUES (?, ?, ?, ?, ?)",
                   (data['id_viaje'], data['lat'], data['lon'], ahora, data['estado']))
    conn.commit()
    conn.close()
    return {"status": "ok"}