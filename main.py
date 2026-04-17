from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Diccionario para guardar lo último de cada chofer
posiciones = {}

@app.route('/iniciar', methods=['GET'])
def iniciar():
    chofer = request.args.get('chofer', 'Chofer_City')
    viaje_id = int(datetime.now().timestamp())
    return jsonify({"id_viaje": viaje_id, "status": "ok"})

@app.route('/gps', methods=['POST'])
def recibir_gps():
    data = request.json
    chofer_name = data.get('chofer', 'Chofer_City')
    
    # IMPORTANTE: Pasamos a mayúsculas y sacamos espacios para que el Monitor lo entienda
    estado_limpio = str(data.get('estado', 'IDA')).upper().strip()

    posiciones[chofer_name] = {
        "chofer": chofer_name,
        "lat": data.get('lat'),
        "lon": data.get('lon'),
        "estado": estado_limpio, 
        "hora": datetime.now().strftime('%H:%M:%S')
    }
    return jsonify({"status": "recibido"})

@app.route('/posiciones_actuales', methods=['GET'])
def enviar_posiciones():
    return jsonify(list(posiciones.values()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
