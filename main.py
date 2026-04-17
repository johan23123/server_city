from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

posiciones = {}

@app.route('/gps', methods=['POST'])
def recibir_gps():
    data = request.json
    chofer = data.get('chofer', 'Chofer_City')
    # ESTO RECIBE LA VUELTA DEL CELU
    estado = str(data.get('estado', 'IDA')).upper().strip()

    posiciones[chofer] = {
        "chofer": chofer,
        "lat": data.get('lat'),
        "lon": data.get('lon'),
        "estado": estado,
        "hora": datetime.now().strftime('%H:%M:%S')
    }
    return jsonify({"status": "ok"})

@app.route('/posiciones_actuales', methods=['GET'])
def enviar_posiciones():
    return jsonify(list(posiciones.values()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
