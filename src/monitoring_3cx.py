#!/usr/bin/env python3

########################################################################
#                   Copyright © by Noah Canadea
########################################################################
#                           Description
#    Python script to get all kind of metrics from a 3cx server api
#
#                    Version 1.0 | 04.04.2022


# import dependencies
from argparse import ArgumentParser
import json
import socket
import requests
import sys

# importing all models
from api_models_3cx_monitoring.trunks import trunks, welcome_from_dict_trunks
from api_models_3cx_monitoring.services import service, welcome_from_dict_services
from api_models_3cx_monitoring.system_status import status, welcome_from_dict_systemstatus

# Config variables
VERSION = "1.0"
MIN_PYTHON_VERSION = (3, 10) # python version 3.10 or higher is required

# global variables
base_url_3cx = None
username = None
password = None
domain = None
tcp_port = None
chacheFolderPath = ""
scriptHealthCheck = False
debugMode = False
chacheTimeInSeconds = 0
auth_cookie = None
session = requests.Session()


def main():
    # global script variables
    global base_url_3cx
    global username
    global password
    global scriptHealthCheck
    global debugMode
    global domain
    global tcp_port

    # exit if python version is too old
    if sys.version_info < MIN_PYTHON_VERSION:
        exitScript(1, "Python version is too old", sys.version_info)

    # getting all arguments
    parser = ArgumentParser(
        description='Zabbix script 3CX monitoring.', add_help=True)
    parser.add_argument('-u', '--username', default='btcadmin',
                        type=str, help='Username to connect with')
    parser.add_argument('-p', '--password', default='btcadmin',
                        type=str, help='Password for the username')
    parser.add_argument('-d', '--domain', type=str,
                        help='Domain of the 3cx server')
    parser.add_argument('-t', '--tcpport', default=443, type=int,
                        help='TCP Port of the 3cx server WebUI')
    parser.add_argument('-c', '--category', type=str,
                        help='The category of the values which should be returned')
    parser.add_argument('--debug', type=bool, default=False,
                        help='prints more information when a error occurs')
    parser.add_argument('--discovery', type=bool,
                        help='flag to set in zabbix discovery mode')  # is not really used in the script itself, but since zabbix requires each item to have a unique key, this is used for the discovery rule
    parser.add_argument('-v', '--version', action='version',
                        version=VERSION, help='Print script version and exit')

    # pharse arguments
    args = parser.parse_args()

    # check if all required arguments are set and exit if not
    if args.username is None or args.password is None or args.domain is None or args.category is None:
        parser.print_help()
        exitScript(1, "Not all required arguments provided", None)

    # set global variables
    username = args.username
    password = args.password
    domain = args.domain
    tcp_port = args.tcpport
    debugMode = args.debug

    # set base url based on https port
    if args.tcpport != 443:
        base_url_3cx = "https://" + \
            str(args.domain) + ":" + str(args.tcpport) + "/api/"
    else:
        base_url_3cx = "https://" + str(args.domain) + "/api/"

    # call ScriptHealtCheck if specified in category-argument
    if args.category == "script-health-check":
        scriptHealthCheck = True
        ScriptHealtCheck()
    else:
        checkPort(domain, tcp_port) # check if port is open before trying to connect to 3cx api
        print(getJsonOfCategory(args.category))

# function that calculates the percentage between two values
def calculatePercentage(used, total) -> float:
    if total == 0:
        return 0
    else:
        return round((used / total) * 100, 2)

# function that takes a category and returns all values of that category as json string
def getJsonOfCategory(category) -> str:
    match category:
        case "3cx-status":
            values = get3CXSystemStatus()
            dic = {
                "FreeMem": values.free_physical_memory,
                "TotalMem": values.total_physical_memory,
                "MemoryUsedPercent": calculatePercentage((values.total_physical_memory - values.free_physical_memory), values.total_physical_memory),
                "CpuUtil": values.cpu_usage,
                "DiskUsedPercent": calculatePercentage((values.total_disk_space - values.free_disk_space), values.total_disk_space),
                "TrunkTot": values.trunks_total,
                "TrunkReg": values.trunks_registered,
                "LicenseActive": values.license_active,
                "CallsActive": values.calls_active,
                "ip_address": values.ip_v4

            }
        case "3cx-info":
            values = get3CXSystemStatus()
            dic = {
                "Autobackup": values.backup_scheduled,
                "IpBlockCount": values.blacklisted_ip_count,
                "LicCode": values.license_key,
                "InstVersion": values.version,
                "LicenseExpireDateUnix": values.expiration_date.timestamp(),
                "3CXFQDN": values.fqdn

            }
        case "3cx-services":
            dic = []
            services = get3CXServices()
            for service in services:
                temp_dic = {
                    "name": service.name,
                    "status": service.status
                }
                dic.append(temp_dic)
        case "3cx-trunks":
            dic = []
            trunks = get3CXTrunks().list
            for trunk in trunks:
                temp_dic = {
                    "name": trunk.name,
                    "registered": trunk.is_registered,
                }
                dic.append(temp_dic)
        case _:
            exitScript(1, "Invalid category argument specified", category)
    try:
        return json.dumps(dic, separators=(',', ':'), default=str)
    except Exception as e:
        exitScript(1, "error while creating json string", e)

# function to get all 3cx services as services object
def get3CXServices() -> service:
    response = getDataFrom3CXAPI('ServiceList')
    try:
        data = welcome_from_dict_services(json.loads(response))
    except Exception as e:
        exitScript(1, "3CX Services parse error", e)
    return data

# function to get all 3cx trunks objects as list
def get3CXTrunks() -> trunks:
    response = getDataFrom3CXAPI('TrunkList')
    try:
        data = welcome_from_dict_trunks(json.loads(response))
    except Exception as e:
        exitScript(1, "3CX Trunks parse error", e)
    return data

# function to get 3cx status as object
def get3CXSystemStatus() -> status:
    response = getDataFrom3CXAPI('SystemStatus')
    try:
        data = welcome_from_dict_systemstatus(json.loads(response))
    except Exception as e:
        exitScript(1, "3CX SystemStatus parse error", e)
    return data

# function that gets the data from the 3cx api on a specific recource url
def getDataFrom3CXAPI(uri) -> str:
    APIauthentication() if auth_cookie is None else None
    try:
        url = base_url_3cx + uri
        headers = {'content-type': 'application/json;charset=UTF-8'}
        response = session.get(url, headers=headers, cookies=auth_cookie)
    except Exception as e:
        exitScript(1, "Error while connecting to 3cx api", e)
    return response.text

# function that gets the access cookie from 3cx api
def APIauthentication() -> None:
    global auth_cookie
    url = base_url_3cx + 'login'
    payload = {'username': username, 'password': password}
    headers = {'content-type': 'application/json'}
    try:
        response = session.post(url, data=json.dumps(
            payload).encode('utf-8'), headers=headers)
    except Exception as e:
        exitScript(1, "Error while connecting to 3cx server api", e)
    if response.status_code == 200 and response.text == 'AuthSuccess':
        cookie = response.cookies
        auth_cookie = cookie
    else:
        exitScript(1, "API authentication error", response.text)

# function to test all components of the script and return the status to the zabbix healthcheck item
def ScriptHealtCheck() -> None:
    # check if installed python version 
    if sys.version_info < MIN_PYTHON_VERSION:
        exitScript(1, "Python version is too old", sys.version_info)
    checkPort(domain, tcp_port)
    testjson1 = getJsonOfCategory("3cx-status")
    testjson2 = getJsonOfCategory("3cx-info")
    testjson3 = getJsonOfCategory("3cx-services")
    testjson4 = getJsonOfCategory("3cx-trunks")
    exitScript(0, "OK", "Script test successful, everything works fine")

# checks if the specified port is open on the remote host
def checkPort(host: str, port: int) -> None:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((host, port))
        s.close()
        return True
    except Exception as e:
        exitScript(1, "Can't connect to " + host + " on Port " + str(port), e)

# function to exit the script with a specific exit code and message
# errors are only printed, if the script is executed in debug mode as healthcheck
def exitScript(exitCode: int, message: str, info) -> None:
    print(message) if scriptHealthCheck and debugMode == False else None
    if debugMode:
        print(message + ": ")
        print(info)
    exit(exitCode)

if __name__ == '__main__':
    main()
