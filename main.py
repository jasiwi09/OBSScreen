#Importamos las librerías necesarias
import pygetwindow as gw
import time
from obswebsocket import obsws, requests
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, url_for, redirect
import json
import threading

#Cargamos dotenv para obtener los dados sensibles desde .env
load_dotenv()

#Nos conectamos al obswebsocket
host = os.getenv("IP")
port = os.getenv("PORT")
password = os.getenv("PASS")
ws = obsws(host, port, password)
ws.connect()

#Lista de variables
scene_name = None
refresh_time = 0.1

jsonFileName = 'apps.json'

f = open(jsonFileName)

kv_array = json.load(f)

f.close()

#Flask APP
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global array
    global kv_array
    if request.method == 'POST':
        new_app = request.form['new_app']
        new_scene = request.form['new_scene']
        kv_array[new_app] = new_scene
        f = open(jsonFileName, 'w')
        json.dump(kv_array, f)
        f.close()
        return redirect(url_for('index'))
    return render_template('index.html', valor=kv_array)



def run_obs_loop():
    while True:
        active_window = gw.getActiveWindow()
        if active_window:
            title = active_window.title.lower()
            try:
                for clave, valor in kv_array.items():
                    if clave in title:
                        scene_name = valor
                        ws.call(requests.SetCurrentProgramScene(sceneName=scene_name))
            except Exception as e:
                print(f"Error {e}")
        else:
            print("No hay ventana activa")
        time.sleep(refresh_time)

    
obs_thread = threading.Thread(target=run_obs_loop)
obs_thread.daemon = True
obs_thread.start()

app.run()








