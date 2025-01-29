import time
import serial
import tkinter as tk
from ui.app import GraphApp  # Importa la clase GraphApp del paquete ui
from tkinter import messagebox

# Función para conectar con Arduino
def arduino_connection():
    try:
        arduino = serial.Serial('COM3', baudrate=9600, timeout=1.0)
        time.sleep(2)
        print("Conectado a Arduino")
        return arduino
    except serial.SerialException:
        print("Error al conectar con Arduino")
    return None

# Función que maneja la interacción con la interfaz
def find_shortest_path_and_send_to_arduino(start, end, graph, arduino):
    # Aquí se calcula el camino más corto usando el método shortest_path de la clase GraphApp
    app = GraphApp(tk.Tk(), arduino)  # Creamos una instancia de GraphApp
    path = app.shortest_path(graph, start, end)  # Usamos el método shortest_path de GraphApp

    if path:
        print(f"Camino más corto: {' -> '.join(path)}")
        
        # Animar el camino en la interfaz de la aplicación
        app.animate_shortest_path(path)  # Animate el camino en la interfaz

        # Enviar la ruta al Arduino paso a paso
        app.send_route_to_arduino(path)  # Enviar la ruta al Arduino
    else:
        print("No se encontró un camino.")

# Main
def main():
    # Conexión con Arduino
    arduino = arduino_connection()
    
    if arduino:
        # Crear la interfaz de usuario (GraphApp)
        root = tk.Tk()
        app = GraphApp(root, arduino)

        # Mostrar la interfaz para que el usuario seleccione los nodos de inicio y fin
        root.mainloop()  # Ejecución de la interfaz gráfica

        # Obtener los nodos seleccionados por el usuario
        start_node = app.start_node_var.get()  # Obtener el valor seleccionado del nodo de inicio
        end_node = app.end_node_var.get()      # Obtener el valor seleccionado del nodo de fin
        
        # Asegurarse de que ambos nodos están seleccionados
        if not start_node or not end_node:
            messagebox.showerror("Error", "Por favor, seleccione tanto el nodo de inicio como el de fin.")
            return

        # Crear el grafo desde la app (GraphApp)
        graph = app.graph  # Grafo dentro de la clase GraphApp

        # Buscar el camino más corto y enviarlo al Arduino
        find_shortest_path_and_send_to_arduino(start_node, end_node, graph, arduino)

if __name__ == "__main__":
    main()
