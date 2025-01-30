import requests
import time

# Reemplaza con la IP del servidor Flask en la PC
SERVER_URL = "http://192.168.3.12:5000/coordenadas"

while True:
    lat = "19.432608"  # Coordenadas simuladas (Ciudad de México)
    lon = "-99.133209"

    try:
        response = requests.get(SERVER_URL, params={'lat': lat, 'lon': lon})
        print("📤 Enviando coordenadas:", lat, lon)
        print("📩 Respuesta del servidor:", response.json())
    except Exception as e:
        print("❌ Error al enviar datos:", e)

    time.sleep(2)  # Esperar 5 segundos antes de volver a enviar
