#!/bin/bash

########################################################################
#         Copyright © by Noah Canadea | All rights reserved
########################################################################
#                           Description
#  Bash Script for installing the 3cx monitoring script on a zabbix server
#
#                    Version 1.0 | 04.04.2022


zabbix_external_scripts_path="/usr/lib/zabbix/externalscripts/"
addon_folder_name="3cx_monitoring"
python_version="python3.9"



trap ctrl_c INT

function ctrl_c() {
    echo ""
    echo -e "\e[31mScript execution manually stopt.\e[39m"

    if [[ $ScriptFolderPath = *"$ProjectFolderName" ]]; then
        rm -r "$ScriptFolderPath"
    fi
    exit 1
}

function OK() {
    echo -e "\e[32m$1\e[39m"
}

function error() {
    echo -e "\e[31m
Error while executing the script.:
$1
Pleas check the shell output.\e[39m"
    exit 1
}

if ! [[ -d $zabbix_external_scripts_path ]]; then
    error "Zabbix script folder not found on this system is the zabbix server installed?"
fi

if ! [[ -x "$(command -v $python_version)" ]]; then
    apt-get install $python_version -y
    OK "$python_version installed"
else
    OK "$python_version already installed"
fi

if ! [[ -x "$(command -v python3-pip)" ]]; then
    apt-get install python3-pip -y
    OK "pip installed"
else
    OK "pip already installed"
fi


pip install -r requirements.txt || error "Error while installing requirements for python"


if ! [[ -d "$zabbix_external_scripts_path" + "$addon_folder_name" ]]; then
    mkdir /etc/$varSmartMonitorFolder
    OK "Zabbix script folder created"
else
    rm -r "$zabbix_external_scripts_path" + "$addon_folder_name" + "/*"
    OK "Old files from zabbix script folder removed"
fi

cp /src/ $zabbix_external_scripts_path + $addon_folder_name + "/" || error "Error while copying files to zabbix script folder"
