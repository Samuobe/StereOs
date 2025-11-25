import os
import subprocess
import threading
import time

# --- Importa modulo CD ---
import function.cd as cd

already_read_disk = 0
global root

def send_notify(data):
    print(data)
    os.system(f'espeak-ng -v it "{data}"')

def check_cd_inserted():
    global already_read_disk
    cd_device = "/dev/sr0"
    if not os.path.exists(cd_device):
        if already_read_disk == 1:
            cd.stop_cd()
            send_notify("Disco rimosso!")
        already_read_disk = 0
        return
    try:
        result = subprocess.run(
            ["udevadm", "info", "--query=property", "--name=sr0"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
        )
        output = result.stdout
        if "ID_CDROM_MEDIA=1" in output:
            if already_read_disk == 0:
                send_notify("CD inserito")
                already_read_disk = 1
                threading.Thread(target=cd.start_cd, daemon=True).start()
        else:
            if already_read_disk == 1:
                cd.stop_cd()
                send_notify("Disco rimosso")
            already_read_disk = 0
    except Exception as e:
        send_notify("Errore nella lettura del cd")

def vlc_telnet():
    # Avvia VLC con interfaccia telnet
    subprocess.Popen([
        "cvlc","-I", "telnet","--telnet-password=ciao", "--telnet-port=4212","--extraintf", "http","--http-password=ciao"
    ])
    time.sleep(2)
    subprocess.run(['curl', '-u', ':ciao', 'http://localhost:8080/requests/status.xml?command=volume&val=200'])

# --- Avvia Flask ---
def start_flask_server():
    subprocess.Popen(["python3", "webserver/server.py"])

# --- Avvia GUI ---
def start_gui():
    subprocess.Popen(["python3", "stereosGUI.py"])
    
# --- MAIN ---
if __name__ == "__main__":
    print("AVVIO CD")
    time.sleep(1)
    send_notify("Stereo avviato")

    # Avvia VLC telnet
    threading.Thread(target=vlc_telnet, daemon=True).start()

    # Avvia server Flask
    threading.Thread(target=start_flask_server, daemon=True).start()

    # Avvia GUI
    threading.Thread(target=start_gui, daemon=True).start()

    # Loop principale controllo CD
    while True:
        check_cd_inserted()
        time.sleep(3)
