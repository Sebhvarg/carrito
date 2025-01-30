from flask import request, jsonify

class LocationService:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule('/location', 'location', self.location, methods=['POST'])

    def location(self):
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
