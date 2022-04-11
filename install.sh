#!/bin/bash

########################################################################
#         Copyright © by Noah Canadea | All rights reserved
########################################################################
#                           Description
#  Bash Script for installing the 3cx monitoring script on a zabbix server
#
#                    Version 1.0 | 11.04.2022

# global variables
zabbix_external_scripts_path="/usr/lib/zabbix/externalscripts/"
project_folder_name="zabbix_3cx_monitoring"
scrip_folder_path="$(dirname -- "$0")"
api_models_folder="api_models_3cx_monitoring"
addon_script_file="monitoring_3cx.py"
api_models_folder_path="${zabbix_external_scripts_path}${api_models_folder}"
addon_script_file_path="${zabbix_external_scripts_path}${addon_script_file}"
data_cache_folder_path="/var/3cx_monitoring_datacache"
python_version="python3.9"



trap ctrl_c INT

# fuction to cancel the script
function ctrl_c() {
    echo ""
    echo -e "\e[31mScript execution manually stopt.\e[39m"

    if [[ $scrip_folder_path = *"$project_folder_name" ]]; then
        rm -r "$scrip_folder_path"
    fi
    exit 1
}

# function to print a confirmation message
function OK() {
    echo -e "\e[32m$1\e[39m"
}

# fuctions to print an error message and stop the script
function error() {
    echo -e "\e[31m
Error while executing the script:
$1
Pleas check the shell output.\e[39m"
    exit 1
}

# check if script is run as root
if (( $EUID != 0 )); then
    error "Pleas run this script with root privileges."
fi

# update apt cache
apt update  || error "Error while updating the apt cache"

# check if the zabbix folder exists on the system
if ! [[ -d $zabbix_external_scripts_path ]]; then
    error "Zabbix script folder not found on this system, is the zabbix server installed?"
fi

# check if the python3.9 is installed and if not install it
if ! [[ -x "$(command -v $python_version)" ]]; then
    apt-get install $python_version -y || error "Error while installing python"
    OK "$python_version installed"
else
    OK "$python_version already installed"
fi

# check if pip is installed and if not install it
if ! [[ -x "$(command -v python3-pip)" ]]; then
    apt-get install python3-pip -y
    OK "pip installed"
else
    OK "pip already installed"
fi

# install python requirements
python3.9 -m pip install -r "$scrip_folder_path/requirements.txt" || error "Error while installing python requirements"

# check if script is allready installed and delete old files if so
if ! [[ -d $api_models_folder_path ]]; then
    mkdir "$api_models_folder_path"
    OK "Folder for api models created"
else
    rm -rfv "$api_models_folder_path/"
    mkdir "$api_models_folder_path"
    OK "Current Installation detected, removing old files"
fi

# copy files to the external script folder
cp -r "$scrip_folder_path/src/$api_models_folder/." "$api_models_folder_path/" || error "Error while copying api models"
cp -r "$scrip_folder_path/src/$addon_script_file" "$zabbix_external_scripts_path" || error "Error while copying api models"

# make script executable
chmod +x "${zabbix_external_scripts_path}${addon_script_file}" || error "Error while assigning execution permission to the script"

OK "------------------------------------------------------"
OK "        Installation finished successfully"
OK "------------------------------------------------------"
