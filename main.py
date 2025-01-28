import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk 
import serial 
import time
from logic.graph import Graph
from logic.pathfinding import shortest_path


# Comunicarse con el arduino

import serial
import time

def arduino_connection():
    try:
        arduino = serial.Serial('COM3', baudrate=9600, timeout=2.0)
        time.sleep(2)  # Asegúrate de darle tiempo a Arduino para establecer la conexión
        print("Conectado a Arduino")
        return arduino
    except serial.SerialException as e:
        print(f"Error al conectar con Arduino: {e}")
        return None



# Enviar ruta optima al arduino

def send_route_to_arduino(arduino, start, end):

    if arduino:
        data = f"{start} - {end} \n"
        arduino.write(data.encode())
        print("Enviando ruta al arduino")
        print("Ruta enviada: ", data)
        return True
    else:
        print("No se pudo enviar la ruta al arduino")
        return False

#Main

def main():
    
    arduino = arduino_connection()
    
    # Crear Grafo 

    graph = Graph()
    graph.add_node("FIEC")
    graph.add_node("FCV")
    graph.add_node("FIMCP")
    graph.add_node("FADCOM")
    graph.add_node("FCNM")

    graph.add_edge("FIEC", "FIMCP", 1)
    graph.add_edge("FIEC", "FCNM", 1)
    graph.add_edge("FIMCP", "FCV", 1)
    graph.add_edge("FCV", "FCNM", 1)
    graph.add_edge("FIMCP", "FCNM", 1)

    ventana = tk.Tk()
    ventana.title("GAYCar")
    ventana.geometry("1200x1600")

    ventana.configure(bg = "black")


if __name__ == "__main__":
    main()
        
    print("Fin de la ejecución")
    

