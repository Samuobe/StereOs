#!/bin/bash


echo "Welcome to the StoreOs installation program!"
echo "What do you want to do?"
echo "1) Install/Update StereOs"
echo "2) Uninstall StereOs"
read -p "Select an option [1/2/5]: " action
read -p "Select an option [1/2/5]: " action

if [[ "$action" == "1" ]]; then
    mkdir stereos-install
    cd stereos-install

    PYTHON_PATH=$(which python3)
    echo 
    echo
    read -p "Install the stable version? (y/n): " choice

    if [[ "$choice" =~ ^[Yy]$ ]]; then
        echo "Installing StereOs stable..."
        sudo pacman -Rns stereos-git
        sudo pacman -Rns stereos-dev-git
        wget https://raw.githubusercontent.com/samuobe/StereOs/main/PKGBUILD/PKGBUILD
        makepkg -si
        rm PKGBUILD
        echo "FINISHED!"       
    else
        echo "Installing StereOs from main branch (beta)..."       
        sudo pacman -Rns stereos-dev-git 
        sudo pacman -Rns stereos
        wget https://raw.githubusercontent.com/samuobe/StereOs/main/PKGBUILD/PKGBUILD-git
        mv PKGBUILD-git PKGBUILD
        makepkg -si        
        rm PKGBUILD
        echo "FINISHED!"        
    fi

    cd ..
    rm -rf stereos-install

elif [[ "$action" == "2" ]]; then
    echo
    echo
    echo "Uninstalling StereOs..."
    sudo pacman -Rns stereos
    sudo pacman -Rns stereos-git
    sudo pacman -Rns stereos-dev-git
    echo "FINISHED!"
elif [[ "$action" == "5" ]]; then
    mkdir stereos-install
    cd stereos-install
    PYTHON_PATH=$(which python3)

    echo "Installing StereOs DEV branch..."
    sudo pacman -Rns stereos 
    sudo pacman -Rns stereos-git
    wget https://raw.githubusercontent.com/samuobe/StereOs/main/PKGBUILD/PKGBUILD-dev
    mv PKGBUILD-dev PKGBUILD
    makepkg -si
    rm PKGBUILD
    echo "FINISHED!" 

    cd ..
    sudo rm -rf stereos-install
fi



rm -- "$0"
