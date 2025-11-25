import os

def start_cd():
    os.system("killall vlc")
    os.system('cvlc --intf http cdda:///dev/sr0 --http-password "ciao"')

def stop_cd():
    import threading
    def kill():
        os.system("killall vlc")
        os.system("cvlc -I telnet --telnet-password=ciao --telnet-port=4212")
    threading.Thread(target=kill, daemon=True).start()