import os
import threading
import time

def start_cd():
    os.system("killall vlc")
    time.sleep(0.3)
    os.system(
        'cvlc cdda:///dev/sr0 '
        '--intf http '
        '--http-password "ciao" '
        '--extraintf telnet '
        '--telnet-password ciao '
        '--telnet-port 4212'
    )

def stop_cd():
    def kill():
        os.system("killall vlc")
        time.sleep(0.3)
        os.system(
            'cvlc '
            '--intf http '
            '--http-password "ciao" '
            '--extraintf telnet '
            '--telnet-password ciao '
            '--telnet-port 4212'
        )
    threading.Thread(target=kill, daemon=True).start()
