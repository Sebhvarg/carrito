import requests

# URL del servidor Flask
url_servidor = "http://192.168.3.12:5000/nodos"

# Obtener los nodos del servidor Flask
def obtener_nodos():
    try:
        response = requests.get(url_servidor)
        
        if response.status_code == 200:
            nodos = response.json()
            print("🌐 Nodos obtenidos:", nodos)
            return nodos
        else:
            print(f"❌ Error al obtener nodos: {response.status_code}")
            return {}
    except Exception as e:
        print(f"⚠️ Error en la solicitud: {e}")
        return {}

# Crear un grafo utilizando los nodos
def crear_grafo(nodos):
    grafo = {}
    
    for nodo_id, nodo in nodos.items():
        lat = nodo["latitud"]
        lon = nodo["longitud"]
        
        # Este ejemplo solo crea un grafo simple con nodos identificados por su ID
        grafo[nodo_id] = {"latitud": lat, "longitud": lon}
    
    print("🗺️ Grafo creado:", grafo)
    return grafo

if __name__ == "__main__":
    nodos = obtener_nodos()
    if nodos:
        grafo = crear_grafo(nodos)
