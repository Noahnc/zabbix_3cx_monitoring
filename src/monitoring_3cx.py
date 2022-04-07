#!/usr/bin/env python3

########################################################################
#         Copyright © by Noah Canadea | All rights reserved
########################################################################
#                           Description
#    Python script to get all kind of metrics from a 3cx server api
#
#                    Version 1.0 | 04.04.2022

from argparse import ArgumentParser
import json
import requests
import os
import time


from api_models_3cx_monitoring.trunks import welcome_from_dict_trunks
from api_models_3cx_monitoring.services import welcome_from_dict_services
from api_models_3cx_monitoring.system_status import welcome_from_dict_systemstatus

VERSION = "1.0"

base_url_3cx = ""
username = ""
password = ""
chacheFolderPath = ""
chacheTimeInSeconds = 0
session = requests.Session()

def main():
    # global script variables
    global base_url_3cx
    global username
    global password

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
    parser.add_argument('-v', '--version', action='version',
                        version=VERSION, help='Print script version and exit')

    # pharse arguments
    args = parser.parse_args()

    # check if all required arguments are set and exit if not
    if args.username is None or args.password is None or args.domain is None or args.category is None:
        parser.print_help()
        exit(1)

    # set global variables
    username = args.username
    password = args.password

    # set base url based on https port
    if args.tcpport != 443:
        base_url_3cx = "https://" + str(args.domain) + ":" + str(args.tcpport) + "/api/"
    else:
        base_url_3cx = "https://" + str(args.domain) + "/api/"

    print(getJsonOfCategory(args.category))

# function that calculates the percentage between two values
def calculatePercentage(used, total):
    if total == 0:
        return 0
    else:
        return round((used / total) * 100, 2)

# function that takes a category and returns all values of that category as json string
def getJsonOfCategory(category):
    match category:
        case "3cx-status":
            values = get3CXSystemStatus()
            dic = {
                "FreeMem": values.free_physical_memory,
                "TotalMem": values.total_physical_memory,
                "FreeMemPercent": calculatePercentage(values.free_physical_memory, values.total_physical_memory),
                "CpuUtil": values.cpu_usage,
                "DiskFreePercent": calculatePercentage(values.free_disk_space, values.total_disk_space),
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
                "MaintenanceExpiryDate": values.expiration_date
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

    return json.dumps(dic, separators=(',', ':'), default=str)

# function to get all 3cx services as services object
def get3CXServices():
    response = getDataFrom3CXAPI('ServiceList')
    data = welcome_from_dict_services(json.loads(response))
    return data

# function to get all 3cx trunks as services object
def get3CXTrunks():
    response = getDataFrom3CXAPI('TrunkList')
    data = welcome_from_dict_trunks(json.loads(response))
    return data

# function to get 3cx status as services object
def get3CXSystemStatus():
    response = getDataFrom3CXAPI('SystemStatus')
    data = welcome_from_dict_systemstatus(json.loads(response))
    return data

# function that gets the data from the 3cx api on a specific recource url
def getDataFrom3CXAPI(uri):
    url = base_url_3cx + uri
    headers = {'content-type': 'application/json;charset=UTF-8'}
    response = session.get(url, headers=headers, cookies=getAccessCookie())
    return response.text

# function that gets the access cookie for the 3cx api
def getAccessCookie():
    url = base_url_3cx + 'login'
    payload = {'username': username, 'password': password}
    headers = {'content-type': 'application/json'}
    response = session.post(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    if response.status_code == 200 and response.text == 'AuthSuccess':
        cookie = response.cookies
        return cookie.get_dict()
    else :
        print("Authentication error, wrong username or password: " + response.text)
        return None

# create a function that takes a filename and a time in seconds and returns true if the file is older than the given time
# def checkIfFileIsOlderThan(self, filename, modifiedTime):
#     if os.path.isfile(self.chacheFolderPath + '/' + filename):
#         file_time = os.path.getmtime(self.chacheFolderPath + '/' + filename)
#         if modifiedTime < (time.time() - file_time):
#             return True
#         else:
#             return False
#     else:
#         return True

# def checkIfCacheFileExists(self, filename):
#     return os.path.isfile(self.chacheFolderPath + '/' + filename)

# def checkIfFolderExists(self):
#     if not os.path.exists(self.chacheFolderPath):
#         os.mkdir(self.chacheFolderPath)

# def saveResponseToCache(self, response, filename):
#     self.checkIfFolderExists()
#     with open(self.chacheFolderPath + "/" + filename, 'w') as outfile:
#         json.dump(json.loads(response), outfile)

# def loadResponseFromCache(self, filename):
#     with open(self.chacheFolderPath + '/' + filename, 'r') as outfile:
#         return json.load(outfile)

if __name__ == '__main__':
    main()