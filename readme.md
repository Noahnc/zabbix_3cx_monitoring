# Zabbix 3CX Monitoring by rest api with python script

The Python sctipt and the zabbix template in this repo allow you to monitor a 3CX Server by rest api.

Tested with Zabbix Version 6.0 on Ubuntu Server 20.04 LTS and 3CX Server 18.


## Setup

1. Connect to your Zabbix Server over ssh.
2. Runn the following install comand:

``` shell
sudo apt update && sudo apt install git -y | \
git clone https://github.com/Noahnc/zabbix_3cx_monitoring.git | \
sudo chmod +x zabbix_3cx_monitoring/install.sh | \
sudo ./zabbix_3cx_monitoring/install.sh
```
3. Test if the scrip works.
``` shell
./usr/lib/zabbix/externalscripts/monitoring_3cx.py -u '<username>' -p '<password>' -d '<3cx domain>' -c "3cx-status"
```
4. Import the zabbix template.
5. Create a new host with the template and specify the required variables


