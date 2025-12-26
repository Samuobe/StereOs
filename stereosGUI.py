import PyQt6.QtWidgets as pq
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QTransform, QPainter, QPainterPath
from PySide6 import QtCore
import sys
import subprocess
import os
import library.lpak as lpak
import glob
import threading
import time
import requests
import musicbrainzngs


#Global vars
data_dir = "/var/lib/stereos/"
data_title_styles = None
data_data_styles = None
remote_control_style_label = None
buttons_style= None
label_cover = None
label_title_artist = None
label_title_title = None
label_title_album = None
label_title_status = None
label_data_artist = None
label_data_title = None
label_data_album = None
label_data_status = None
data_layout = None
root = None
language = None
status = None
cover_pixmap = None
old_copertina = None
bluetooth_default = None
current_angle = 0
copertina = "Get"

#Auto set variable
avaible_languages_temp = glob.glob(f"./lpak/*.lpak")
avaible_languages = []
for lang in avaible_languages_temp:
    avaible_languages.append(lang.split("/")[2].split(".")[0])

def load_config():
    global language, bluetooth_default, data_dir
    config_file = data_dir+"stereos.conf"

    def generate_new_config_file(config_file):
        with open(config_file, "w") as f:
            f.write("Language=English\n")
            f.write("BluetoothDefault=Off")
    
    # Check if the file exists and is a file
    if not os.path.isfile(config_file):
        generate_new_config_file(config_file)

    with open(config_file) as f:
        data = f.readlines()
    print(data)
    try:
        language = data[0].split("=")[1].strip()
        bluetooth_default =data[1].split("=")[1].strip()
    except:
        generate_new_config_file(config_file)



def def_styles():
    global data_title_styles, data_data_styles, remote_control_style_label, buttons_style
    data_title_styles = '''
    QLabel {
        color: #ff5555;                /* colore rosso acceso */
        font-family: "Arial Black";    /* nome del font */
        font-size: 30pt;               /* dimensione del testo */
        font-weight: bold;             /* grassetto */
    }
    '''

    data_data_styles = '''
    QLabel {
        color: #00cc66;                /* verde */
        font-family: "Segoe UI";       /* font moderno */
        font-size: 30pt;               /* leggermente più piccolo */
    }
    '''

    remote_control_style_label=data_data_styles = '''
                                                QLabel {
                                                    color: #10C0E0;              
                                                    font-family: "Segoe UI";
                                                    font-size: 30pt;    
                                                }
                                                '''

    buttons_style ="""
            QPushButton {
                font-size: 40pt;
                padding: 5px;
                border-radius: 10px;
                background-color: #333;
                color: white;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """

def generate_data_interface():
    global data_layout, label_cover
    global label_title_artist, label_title_title, label_title_album, label_title_status
    global label_data_artist, label_data_title, label_data_album, label_data_status
    #Cover
    # --- Cover ---
    label_cover = pq.QLabel()
    label_cover.setFixedSize(128, 128)
    default_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "icons/no_media.png"))

    pixmap = QPixmap(default_path)
    if pixmap.isNull():
        pixmap = QPixmap(128, 128)
        pixmap.fill(Qt.GlobalColor.gray)
        print("ERROR WHIT PIXAMP")
    else:
        label_cover.setPixmap(pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio))


    #Text data
    label_title_artist = pq.QLabel()
    label_title_title = pq.QLabel()
    label_title_album= pq.QLabel()
    label_title_status = pq.QLabel()

    label_data_artist = pq.QLabel()
    label_data_title = pq.QLabel()
    label_data_album= pq.QLabel()
    label_data_status = pq.QLabel()

    data_layout.addWidget(label_cover, 0, 4, 4, 1, alignment=Qt.AlignmentFlag.AlignRight)  

    data_layout.addWidget(label_title_artist, 0, 0)
    data_layout.addWidget(label_data_artist, 0, 1)
    data_layout.addWidget(label_title_title, 1, 0)
    data_layout.addWidget(label_data_title, 1, 1)
    data_layout.addWidget(label_title_album, 2, 0)
    data_layout.addWidget(label_data_album, 2, 1)
    data_layout.addWidget(label_title_status, 3, 0)
    data_layout.addWidget(label_data_status, 3, 1)



    data_layout.setColumnStretch(data_layout.columnCount(), 2)
    data_layout.setRowStretch(data_layout.rowCount(), 1)
    data_layout.setHorizontalSpacing(0) 

    data_layout.setHorizontalSpacing(20)  # aumenta distanza orizzontale
    data_layout.setContentsMargins(20, 0, 20, 0)  # margini extra

    root.repaint()

def update_data():
    def get_cover_web(artist, title, album):
        musicbrainzngs.set_useragent(
            "SonneMusic",      
            "1.0",
            "https://github.com/Samuobe/StereOs"
        )

        def cerca_brano(titolo, artista=None, album=None):
            query = titolo
            if artista:
                query += f' AND artist:"{artista}"'
            if album:
                query += f' AND release:"{album}"'

            result = musicbrainzngs.search_recordings(
                query=query,
                limit=1
            )

            if not result["recording-list"]:
                return None

            recording = result["recording-list"][0]

            release = recording["release-list"][0]
            
            return {
                "titolo": recording["title"],
                "artista": recording["artist-credit"][0]["artist"]["name"],
                "album": release["title"],
                "release_id": release["id"]
            }

            def get_cover_url(release_id):
                url = f"https://coverartarchive.org/release/{release_id}"
                r = requests.get(url)

                if r.status_code != 200:
                    return None

                data = r.json()

                for img in data["images"]:
                    if img.get("front"):
                        return img["image"]  # URL immagine

                return None
        brano = cerca_brano(
            titolo="White Wolf",
            artista="Roses of Thieves",
            album="Demons Ascend"
        )

        if brano:
            cover_url = get_cover_url(brano["release_id"])
            
            print("Titolo:", brano["titolo"])
            print("Artista:", brano["artista"])
            print("Album:", brano["album"])
            print("Copertina:", cover_url)

            return cover_url
        else:
            return("")
    
    global data_layout, label_cover
    global label_title_artist, label_title_title, label_title_album, label_title_status
    global label_data_artist, label_data_title, label_data_album, label_data_status
    global data_title_styles, data_data_styles, copertina, status, cover_pixmap, default_image_status, copertina_status
    global old_copertina, scaled_cover_pixmap
    artist = title = album = position = status = volume = duration = ""
    command_string = "playerctl metadata --format '{{xesam:artist}}|||{{xesam:title}}|||{{xesam:album}}|||{{position}}|||{{status}}|||{{volume}}|||{{duration}}|||{{playerName}}'"
    command = []
    command = command_string.split(" ")
    data = subprocess.run(command, capture_output=True, text=True).stdout
    data =data[1:-1]
    data_list=data.split("|||")
    test_data = len(data_list)
    if test_data < 3:
        artist = "No data"
        title = "No data"
        album = "No data"
        position = "No data"
        status = "No data" 
        volume = "No data"
        duration = "No data"

        label_data_title.setText("")
        label_title_title.setText("")
        label_data_album.setText("")
        label_title_album.setText("")
        label_title_status.setText("")
        label_data_status.setText("")


        label_title_artist.setText(lpak.get("No media", language))
        label_title_artist.setStyleSheet(data_title_styles)
        label_data_artist.setText("")
        copertina = "No data"
        copertina_status = False

    else:
        data =data[1:-1]
        artist, title, album, position, status, volume, duration, player = data_list


        def generate_standar_data(artist, title, album, status):
            global data_title_styles, data_data_styles
            try:
                label_data_album.setText("")                
                pass
            except:
                generate_data_interface()
            label_title_artist.setText(lpak.get("Artist", language)+":   ")
            label_title_title.setText(lpak.get("Title", language)+":   ")
            label_title_album.setText(lpak.get("Album", language)+":   ")
            label_title_status.setText(lpak.get("Status", language)+":   ")            

            label_data_artist.setText(artist)
            label_data_title.setText(title)
            label_data_album.setText(album)
            label_data_status.setText(status)

            label_title_artist.setStyleSheet(data_title_styles)
            label_title_title.setStyleSheet(data_title_styles)
            label_title_album.setStyleSheet(data_title_styles)
            label_title_status.setStyleSheet(data_title_styles)
            label_data_artist.setStyleSheet(data_data_styles)
            label_data_title.setStyleSheet(data_data_styles)
            label_data_album.setStyleSheet(data_data_styles)
            label_data_status.setStyleSheet(data_data_styles)
        if "Music Assistant" == title:
            copertina = "Music Assistant"
                      
            label_data_title.setText("")
            label_title_title.setText("")
            label_data_album.setText("")
            label_title_album.setText("")
            #label_title_status.setText("")
            #label_data_status.setText("")

            label_title_artist.setStyleSheet(remote_control_style_label)
            label_data_artist.setStyleSheet(remote_control_style_label)

            label_title_artist.setText(lpak.get("Controlled whit", language)+" ")
            label_data_artist.setText("Music Assistant")
            label_title_status.setText(lpak.get("Status", language)+":   ")
            label_title_status.setStyleSheet(remote_control_style_label)
            label_data_status.setText(status)
        elif "vlc" in player: 
            copertina = "Vlc"
            generate_standar_data(artist, title, album, status)
            
        else:
            copertina = "Bluetooth"                      
            generate_standar_data(artist, title, album, status)   

    # --- Copertina ---
    copertina_status = True
    cover_pixmap = QPixmap()  
    if copertina == "Vlc":
        try:
            cover = subprocess.run(["playerctl", "metadata", "mpris:artUrl"],
                                capture_output=True, text=True)
            path = cover.stdout.strip()

            if not path:  # se non c'è nulla in riproduzione
                raise ValueError("Nessuna cover trovata")

            if path.startswith("file://"):
                path = path.replace("file://", "")
                

            if path.startswith("http"):
                response = requests.get(path)
                if response.status_code == 200:
                    cover_pixmap.loadFromData(response.content)
                    copertina = "File_web"
            else:
                copertina = "File"
                cover_pixmap.load(path)

        except Exception:
            if copertina == "No data":
                default_path = os.path.join(os.path.dirname(__file__), "icons/no_media.png")
                copertina = "No data"
            else:
                #cerca online, altrimenti default
                path = get_cover_web(artist, title, album)
                if path.startswith("http") and path != "":
                    response = requests.get(path)
                    if response.status_code == 200:
                        cover_pixmap.loadFromData(response.content)
                        copertina = "File_web"
                else:
                    path = os.path.join(os.path.dirname(__file__), "icons/default_cd.png")
                    copertina = "Default CD"
            cover_pixmap.load(path)
            default_image_status = True
    else:
        if copertina == "Music Assistant":
            path = os.path.join(os.path.dirname(__file__), "icons/music_assistant.png")
            cover_pixmap.load(path)
        elif copertina == "Bluetooth":
            path = os.path.join(os.path.dirname(__file__), "icons/bluetooth.png")
            cover_pixmap.load(path)
        else:
            path = os.path.join(os.path.dirname(__file__), "icons/no_media.png")
            cover_pixmap.load(path)

    # Aggiorna QLabel della cover
    if copertina != old_copertina:     
        if not cover_pixmap.isNull():    
            old_copertina = copertina
            scaled_cover_pixmap = cover_pixmap.scaled(
            128, 128,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        cover_pixmap = scaled_cover_pixmap
        label_cover.setPixmap(scaled_cover_pixmap)
    
        


    root.repaint()
    return artist, title, album, position, status, volume, duration;    

def rotate_cover():
    global current_angle, label_cover, status, cover_pixmap, copertina
    if cover_pixmap is None:
        return
    if copertina == "Bluetooth":        
        return
    if status != "Playing":
        return
    

    current_angle = (current_angle + 1) % 360

    size = 128  # dimensione fissa del QLabel
    rotated_pixmap = QPixmap(size, size)
    rotated_pixmap.fill(Qt.GlobalColor.transparent)

    # ruota l'immagine originale
    transform = QTransform()
    transform.rotate(current_angle)
    rotated = cover_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)

    # centra l'immagine ruotata nel pixmap fisso
    painter = QPainter(rotated_pixmap)
    x = (size - rotated.width()) // 2
    y = (size - rotated.height()) // 2
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # crea una maschera circolare
    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    painter.setClipPath(path)

    # disegna l'immagine centrata
    painter.drawPixmap(x, y, rotated)
    painter.end()

    # imposta pixmap sulla QLabel
    label_cover.setPixmap(rotated_pixmap)
    label_cover.setStyleSheet("QLabel { border-radius: 64px; border: 0px solid #888; }")

#bridge
def run_bluetooth_bridge():
    command = ["bash", "function/bluetooth_playerctl_bridge.sh"]  # esempio
    try:
        # subprocess.run blocca finché non finisce, ma è in thread quindi UI OK
        result = subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        print("Error stating bridge:", e)

# Avvio in un thread
bluetooth_bridge = threading.Thread(target=run_bluetooth_bridge)
bluetooth_bridge.start()



def test():
    update_data()
    exit()

#####GUI functions

#Buttons functions
def play():
    os.system("playerctl play")
    update_data()
def pause():
    os.system("playerctl pause")
    update_data()
def next_song():
    os.system("playerctl next")
    update_data()
def prev_song():
    os.system("playerctl previous")
def volume_più():
    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"])

def volume_down():
    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"])
def expel_cd():
    os.system("eject")
    update_data()


def bluetooth_is_powered():
        try:
            # Lancia bluetoothctl show
            result = subprocess.run(
                ["bluetoothctl", "show"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = result.stdout

            # Cerca la riga Powered
            for line in output.splitlines():
                line = line.strip()
                if line.startswith("Powered:"):
                    # True se yes, False se no
                    return line.split()[1].lower() == "yes"

            # Se non trovi Powered
            return False

        except FileNotFoundError:
            print("Errore: bluetoothctl non trovato")
            return False
def enable_bluetooth():   
    if bluetooth_is_powered():
        button_enable_disable_bluetooth.setText("📵")
        os.system("bluetoothctl power off")
    else:
        button_enable_disable_bluetooth.setText("📱")
        os.system("rfkill unblock bluetooth")
        os.system("bluetoothctl power on")

#test()

###########
###START###
###########
load_config()
def_styles()
#BASE
app = pq.QApplication(sys.argv)
root = pq.QMainWindow()
root.showFullScreen()
#root.showMaximized()

#Update data timer 
timer_data = QtCore.QTimer()
timer_data.timeout.connect(update_data) 
timer_data.start(500) 
#Rotate cover timer
cover_timer = QtCore.QTimer()
cover_timer.timeout.connect(rotate_cover)
cover_timer.start(16)

central_widget = pq.QWidget()   #layout
root.setCentralWidget(central_widget)
main_layout = pq.QVBoxLayout(central_widget)

#Data
data_layout = pq.QGridLayout()

generate_data_interface()

main_layout.addLayout(data_layout)



#Buttons

buttonX=300
buttonY=100

button_play = pq.QPushButton(text="▶️")
button_play.pressed.connect(play)
button_play.setFixedSize(buttonX, buttonY)
button_play.setStyleSheet(buttons_style)

button_pause = pq.QPushButton(text="⏸️")
button_pause.pressed.connect(pause)
button_pause.setFixedSize(buttonX, buttonY)
button_pause.setStyleSheet(buttons_style)

button_next_song=pq.QPushButton(text="⏭️")
button_next_song.pressed.connect(next_song)
button_next_song.setFixedSize(buttonX, buttonY)
button_next_song.setStyleSheet(buttons_style)

button_prev_song = pq.QPushButton(text="⏮️")
button_prev_song.pressed.connect(prev_song)
button_prev_song.setFixedSize(buttonX, buttonY)
button_prev_song.setStyleSheet(buttons_style)

button_vol_più = pq.QPushButton(text="🔊")
button_vol_più.pressed.connect(volume_più)
button_vol_più.setFixedSize(buttonX, buttonY)
button_vol_più.setStyleSheet(buttons_style)

button_vol_down = pq.QPushButton(text="🔉")
button_vol_down.pressed.connect(volume_down)
button_vol_down.setFixedSize(buttonX, buttonY)
button_vol_down.setStyleSheet(buttons_style)

button_expel_cd = pq.QPushButton(text="💿")
button_expel_cd.pressed.connect(expel_cd)
button_expel_cd.setFixedSize(buttonX, buttonY)
button_expel_cd.setStyleSheet(buttons_style)

button_enable_disable_bluetooth = pq.QPushButton()
button_enable_disable_bluetooth.pressed.connect(enable_bluetooth)
button_enable_disable_bluetooth.setFixedSize(buttonX, buttonY)
button_enable_disable_bluetooth.setStyleSheet(buttons_style)

commands_layout = pq.QGridLayout()
commands_layout.addWidget(button_prev_song,    0, 0)
commands_layout.addWidget(button_play, 0, 1)
commands_layout.addWidget(button_pause,   0, 2)
commands_layout.addWidget(button_next_song,  0, 3)
commands_layout.addWidget(button_vol_più, 1, 0)
commands_layout.addWidget(button_expel_cd,  1, 1)
commands_layout.addWidget(button_enable_disable_bluetooth, 1, 2)
commands_layout.addWidget(button_vol_down,   1, 3)
   

main_layout.addLayout(commands_layout)

if bluetooth_default == "On":
    os.system("bluetoothctl power on")
else:
    os.system("bluetoothctl power off")

if bluetooth_is_powered():
    button_enable_disable_bluetooth.setText("📱")
else:    
    button_enable_disable_bluetooth.setText("📵")



##Top bar
def poweroff_command():
    os.system("poweroff")
def close_stereos():
    os.system("killall vlc")
    os._exit(0)
    exit()
    
def change_language(new_language):
    global language
    language = new_language
    generate_menu(menu_bar)
    with open(data_dir+"stereos.conf", "w") as f:
        f.write("Language="+new_language)
def bluetooth_settings():
    os.system("blueman-manager &") 
    
    


#DEF MENU
def generate_menu(menu_bar):
    menu_bar.clear()  
    #
    stereos_settings_menu = menu_bar.addMenu(lpak.get("Settings", language))
    language_menu = stereos_settings_menu.addMenu(lpak.get("Languages", language))
    for lang in avaible_languages:
        language_button=language_menu.addAction(lang)
        language_button.triggered.connect(lambda checked, l=lang: change_language(l))
    bluetooth_settings_button = stereos_settings_menu.addAction(lpak.get("Bluetooth settings", language))
    bluetooth_settings_button.triggered.connect(bluetooth_settings)


    system_menu = menu_bar.addMenu(lpak.get("System", language))
    poweroff_action = system_menu.addAction(lpak.get("Shutdown", language))
    poweroff_action.triggered.connect(poweroff_command)
    close_stereos_button = system_menu.addAction(lpak.get("Exit", language))
    close_stereos_button.triggered.connect(close_stereos)
    #
menu_bar = root.menuBar()
generate_menu(menu_bar)




root.show()
sys.exit(app.exec())
