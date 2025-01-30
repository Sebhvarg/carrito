from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/location', methods=['POST'])
def location():
    try:
        # Obtener los datos enviados como JSON
        data = request.get_json()

        # Depuración: Imprimir los datos recibidos
        print(f"Datos recibidos: {data}")

        # Comprobar si los datos fueron recibidos
        if data:
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if latitude is not None and longitude is not None:
                print(f"Recibido: Latitud = {latitude}, Longitud = {longitude}")
                return jsonify({"message": "Ubicación recibida exitosamente"}), 200
            else:
                print("Error: Datos de ubicación incompletos")
                return jsonify({"error": "Datos de ubicación incompletos"}), 400
        else:
            print("Error: No se recibieron datos")
            return jsonify({"error": "No se recibieron datos"}), 400
    except Exception as e:
        print(f"Error en el servidor Flask: {e}")
        return jsonify({"error": f"Ocurrió un error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Activa el modo debug
