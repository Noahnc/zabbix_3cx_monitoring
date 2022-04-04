from argparse import ArgumentParser
import json
from nis import match
from DataController import data_handler
from DataController import api_handler

data = data_handler()
VERSION = 0.5
    
def main():
    parser = ArgumentParser(description='Zabbix script 3CX monitoring.', add_help=True)
    parser.add_argument('-u', '--username', default='btcadmin', type=str, help='Username to connect with')
    parser.add_argument('-p', '--password', default='btcadmin', type=str, help='Password for the username')
    parser.add_argument('-d', '--domain', type=str, help='Domain of the 3cx server')
    parser.add_argument('-c', '--category', type=str, help='The category of the values which should be returned')
    parser.add_argument('-t', '--time', default=30, type=int, help='time in seconds how long the 3cx data should be cached')
    parser.add_argument('-v', '--version', action='version', version=VERSION, help='Print script version and exit')


    args = parser.parse_args()


    # check if all arguments are set
    if args.username is None or args.password is None or args.domain is None or args.category is None:
        parser.print_help()
        exit(1)
    else:
        api = api_handler(args.username, args.password, args.domain)
        data.setup(api, args.time)
        print(getJsonOfCategory(args.category))


def calculatePercentage(used, total):
    if total == 0:
        return 0
    else:
        return round((used / total) * 100, 2)


def getJsonOfCategory(category):
    match category:
        case "3cx-status":
            dic = {
                "FreeMem": data.get3CXSystemStatus().free_physical_memory,
                "TotalMem": data.get3CXSystemStatus().total_physical_memory,
                "FreeMemPercent": calculatePercentage(data.get3CXSystemStatus().free_physical_memory, data.get3CXSystemStatus().total_physical_memory),
                "CpuUtil": data.get3CXSystemStatus().cpu_usage,
                "DiskFreePercent": calculatePercentage(data.get3CXSystemStatus().free_disk_space, data.get3CXSystemStatus().total_disk_space),
                "TrunkTot": data.get3CXSystemStatus().trunks_total,
                "TrunkReg": data.get3CXSystemStatus().trunks_registered
            }
        case "3cx-info":
            dic = {
                "Autobackup": data.get3CXSystemStatus().backup_scheduled,
                "IpBlockCount": data.get3CXSystemStatus().blacklisted_ip_count,
                "LicCode": data.get3CXSystemStatus().license_key,
                "InstVersion": data.get3CXSystemStatus().version
            }
        case "3cx-services":
            dic = []
            for service in data.get3CXServices():
                temp_dic = {
                    "name": service.name,
                    "status": service.status
                }
                dic.append(temp_dic)

    return json.dumps(dic, separators=(',', ':'))



if __name__ == '__main__':
    main()


