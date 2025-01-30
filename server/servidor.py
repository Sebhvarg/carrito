from flask import Flask, request

app = Flask(__name__)

# Ruta donde se guardarán las coordenadas
FILE_PATH = "coordenadas.txt"

@app.route('/coordenadas', methods=['GET'])
def recibir_coordenadas():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if lat and lon:
        print(f"📍 Coordenadas recibidas: Latitud = {lat}, Longitud = {lon} \n")

        # Guardar coordenadas en un archivo de texto
        with open(FILE_PATH, "a") as file:
            file.write(f"{lat},{lon}\n")

        return {"status": "OK", "latitud": lat, "longitud": lon}, 200
    else:
        return {"error": "Faltan parámetros lat y lon"}, 400

if __name__ == '__main__':
    app.run(host='192.168.3.12', port=5000)
