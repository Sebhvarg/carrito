from flask import Flask, request

app = Flask(__name__)

#Guardar en un diccionario las latitudes y longitudes

nodos = {}

cantidad = 0

@app.route('/coordenadas', methods=['GET'])

def recibir_coordenadas():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if lat and lon:
        print(f"📍 Coordenadas recibidas: Latitud = {lat}, Longitud = {lon}")
        nodos[cantidad] = {"latitud": lat, "longitud": lon}
        cantidad += 1        
        return {"status": "OK", "latitud": lat, "longitud": lon}, 200
    else:
        return {"error": "Faltan parámetros lat y lon"}, 400
    
    
def obtener_nodos():
    return nodos

#Exportar diccionario de nodos
@app.route('/nodos', methods=['GET'])
def exportar_nodos():
    return obtener_nodos(), 200


if __name__ == '__main__':
    app.run(host='192.168.3.12', port=5000)
    