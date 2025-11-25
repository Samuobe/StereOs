from flask import Flask, render_template, request, redirect 
import os
import alsaaudio
import subprocess  # aggiungi questa importazione
import requests
import threading
import xml.etree.ElementTree as ET

app = Flask(__name__)

current_youtube_id = "dQw4w9WgXcQ"  # esempio (Rickroll 😁)


@app.route('/execute', methods=['POST'])
def esegui():
    action = request.form.get('action')    
    if action == 'play_or_pause':
        print("PLAY PAUSE")
        # Leggi lo stato attuale con requests (senza inviare comandi)
        try:
            response = requests.get("http://localhost:8080/requests/status.xml", auth=('', 'ciao'))
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                state = root.findtext('state')
                if state == "playing":
                    os.system('curl -u :ciao "http://localhost:8080/requests/status.xml?command=pl_pause"')
                else:
                    os.system('curl -u :ciao "http://localhost:8080/requests/status.xml?command=pl_play"')
        except Exception as e:
            print("Errore nel play/pause:", e)
    elif action == 'next_song':
        print("NEXT")
        os.system('curl -u :ciao "http://localhost:8080/requests/status.xml?command=pl_next"')
    elif action == "previous_song":
        print("PRE")
        os.system('curl -u :ciao "http://localhost:8080/requests/status.xml?command=pl_previous"')
    elif action == "volume_down":
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"])
    elif action == "volume_up":
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"])
    elif action == "eject_disk":
        os.system("eject")


    else:
        print("Nessun comando riconosciuto")

    return redirect("/")

current_youtube_proc = None


@app.route("/", methods=['GET', 'POST'])
def home_page():
    global old_title
    # cambia anche il video YouTube
    
    
    try:
        response = requests.get("http://localhost:8080/requests/status.xml", auth=('', 'ciao'))
        title = artist = album = "No disk"
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            meta = root.find(".//information/category[@name='meta']")
            if meta is not None:
                for info in meta.findall("info"):
                    name = info.attrib.get("name", "")
                    if name == "title":                        
                        title = info.text or "No disk"
                        old_title = title
                    elif name == "artist":
                        artist = info.text or "No disk"
                    elif name == "album":
                        album = info.text or "No disk"
    except Exception:
        title = "No disk"
        artist = "No disk"
        album = "No disk"

    return render_template(
        "home.html",
        title=title,
        artist=artist,
        album=album,
        youtube_id=current_youtube_id
    )
        

def start():  
    app.run(host="0.0.0.0", ssl_context=("cert.pem", "key.pem"), use_reloader=False)
    

start()