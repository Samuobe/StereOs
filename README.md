
# StereOs

Hey! Are you also passionate about CDs? Does your PC struggle to play music while you're browsing? Do you want to finally take advantage of Home Assistant and Music Assistant and use your phone at the same time? Perfect! This is the right app for you, created for all these reasons (yes, I hit the jackpot)!


## Features
StereOs offers many features: 
- CD reader support: Connect a CD player to your computer to listen to it!
- Music Assistant & Home Assistant: Using VLC telnet, you can stream music to your new stereo via Home Assistant and Music Assistant!
- Bluetooth audio: Going to the Bluetooth settings will open Blueman (https://github.com/blueman-project/blueman) for managing Bluetooth devices 
- GUI screen: The main screen has the controls you need, including CD eject and Bluetooth activation or deactivation.
- Web control: StereOs also has an https web interface for remote music control.
- Multi language: StereOs supports multiple languages! I look forward to your help in expanding them.

## Installation
I have made installation very simple. Just run this command and choose which version to install: 

```bash
    curl -LO https://raw.githubusercontent.com/Samuobe/StereOs/main/install.sh && bash install.sh
```

## Instruction

### On the main screen, we see three sections: 

### Top bar

<img width="365" height="179" alt="menu lingue" src="https://github.com/user-attachments/assets/9706e863-2771-4a85-a8ee-7bdbe1a14cec" />

In the top bar, we have “System” and “Settings.”
- System: Contains two options: closing StereOs and shutting down the system.
- Settings: This also has two options: Bluetooth settings and immediate language change.

### Music information
Every second, this screen updates with new song data. The image shows where the audio is coming from: the Bluetooth symbol for Bluetooth, the Music Assistant symbol for Music Assistant, and a disc symbol for when a CD is inserted.

### Buttons bar

<img width="1440" height="900" alt="home" src="https://github.com/user-attachments/assets/8660eefc-361e-4ed8-b166-7dd84d75411e" />

We have 8 buttons:
- ⏮️: Previus song
- ▶️: Restart music
- ⏸️: Pause music
- ⏭️: Next song
- 🔊: Volume up
- 💿: Eject the disk
- 📱/📵: Enable/Disable bluetooth (📱=Enable | 📵=Disable)
- 🔉: Volume down
## Screenshots

<img width="2206" height="1461" alt="web" src="https://github.com/user-attachments/assets/66606a73-6584-4b44-9ee1-cdfcead8d245" />
<img width="1440" height="900" alt="HA" src="https://github.com/user-attachments/assets/a4256393-8756-40c3-98c7-62e9541e6e9d" />
<img width="1440" height="900" alt="CD" src="https://github.com/user-attachments/assets/5a3f2a35-5806-408a-a1e8-bc39d6831138" />
<img width="1440" height="900" alt="BLUETOOTH" src="https://github.com/user-attachments/assets/32b9b903-2926-455b-a4f6-b98d0f9a0a95" />

## Contribute
Contributions are welcome! Especially with the language, to contribute you need to fork the repository, modify it, and send a pull request.

### Language contribute
Contributing to the language is easy. First, clone the repository, then:
1) Check if a file for your language already exists. If not, create it in the “lpak” subfolder and name it using the language name in that language + .lpak. For example, the Italian language is “Italiano” in Italian and ‘Italian’ in English, so I will name the file “Italiano.lpak.”
2) Take the missing entries from the “English.lpak” file and copy them into it.
3) Replace ONLY THE WORDS AFTER THE PIPE SYMBOL (|), that will be the translation.
4) Send the pull request and wait for approval!

If there are any problems, don't hesitate to open an issue!

### Suggestions, requests, bugs
For any reports, problems, requests, or suggestions, please use GitHub issues, or feel free to fork and fix! It's best to let us know first, so we don't accidentally work on the same thing!


## Contact
You can contact me via GitHub issues, or by email at samuobe@outlook.com.
