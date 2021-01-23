#!/bin/bash

kvm_dialog(){
    printf "Are you wan't to enable kvm?[Y/n]: "
    read -r kvm

    if [ "$kvm" == "y" ]; then
        echo "\n \e[31m[ ]\e[0mInstalling qemu-kvm..."
        sudo apt install qemu-kvm
        
        if [ $? != 0 ]; then
            echo "[\e[31m] Can't install required package: qemu-kvm. Exited with status $?"
        else
            echo -e "[\e[32m*\e[0m] Package: qemu-kvm - installed succefly!"
        fi
    else
        echo "Continue Downloading process with no kvm..."
    fi
}

pkg(){

    echo "installing $1"
    sudo apt install $1
    if [ $? != 0 ]; then
        echo -e "\[\e[31m] Can't install required package: $1. Exited with status $?"
    else
        echo -e "[\e[32m*\e[0m] Package: $1 - installed succefly!"
    fi
}
clear
echo -e "\n\e[31m[ ]\e[0m installing required packages... \n"
pkg qemu
kvm_dialog
echo ""



echo "Qemu-TUI. All rights not reserved 2021-2021"













