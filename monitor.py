from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Diccionario para guardar lo último de cada chofer
posiciones = {}

@app.route('/iniciar', methods=['GET'])
def iniciar():
    chofer = request.args.get('chofer', 'Anonimo')
    viaje_id = int(datetime.now().timestamp())
    return jsonify({"id_viaje": viaje_id, "status": "ok"})

@app.route('/gps', methods=['POST'])
def recibir_gps():
    data = request.json
    chofer_name = "Chofer_City" # O podés recibirlo en el JSON
    
    # GUARDAMOS TODO: lat, lon y el ESTADO dinámico que viene del celu
    posiciones[chofer_name] = {
        "chofer": chofer_name,
        "lat": data.get('lat'),
        "lon": data.get('lon'),
        "estado": data.get('estado', 'S/D').upper(), # ACÁ SE RECIBE EL "VUELTA"
        "hora": datetime.now().strftime('%H:%M:%S')
    }
    print(f"Recibido: {posiciones[chofer_name]}")
    return jsonify({"status": "recibido"})

@app.route('/posiciones_actuales', methods=['GET'])
def enviar_posiciones():
    return jsonify(list(posiciones.values()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
