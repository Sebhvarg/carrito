import tkinter as tk 
from ui.app import App
import serial # type: ignore
import time
# Comunicarse con el arduino

def arduino_connection():
    try:
        arduino = serial.Serial('COM3', baudrate= 9600, timeout=1.0)
        time.sleep(2)
        print("Conectado a Arduino")
        return arduino
    except: serial.SerialException
    print("Error al conectar con Arduino")
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
