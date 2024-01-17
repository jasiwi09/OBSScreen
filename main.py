import pygetwindow as gw
import time
from obswebsocket import obsws, requests


mi_diccionario = {
    "chrome": "Time",
    "fivem": "GTA2"
}


host = "192.168.0.160"
port = 4455
password = "RDLcLWfvhAvEREyg"
nombre_de_la_escena = None

ws = obsws(host, port, password)
ws.connect()

while True:
    active_window = gw.getActiveWindow()
    if active_window:
        title = active_window.title.lower()
        print('Title: ', title)
        try:
            for clave, valor in mi_diccionario.items():
                print('Clave: ', clave, ' Valor: ', valor)
                #print(f"Clave: {clave}, Valor: {valor}")

                if clave in title:
                    nombre_de_la_escena = valor
                    print(f"Estás en la ventana {clave} y se va a activar {valor}")

                    ws.call(requests.SetCurrentProgramScene(sceneName=nombre_de_la_escena))
                    print(f"Cambiado a la escena: {nombre_de_la_escena}")
                else:
                    print("No estás en ninguna ventana que está en la lista")
        except Exception as e:
            print(f"Error {e}")
        """try:
            if "chrome" in title:
                nombre_de_la_escena = "Time"
                print("Estás en Google Chrome")
            elif "fivem" in title:
                nombre_de_la_escena = "GTA2"
                print("Estás en FiveM")
            else:
                print("No estás en Chrome ni en VS Code")
            ws.call(requests.SetCurrentProgramScene(sceneName=nombre_de_la_escena))
            print(f"Cambiado a la escena: {nombre_de_la_escena}")
        except Exception as e:
            print(f"Error: {e}")"""
    else:
        print("No hay ventana activa")

    time.sleep(1)





