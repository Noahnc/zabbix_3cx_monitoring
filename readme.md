# Zabbix 3CX Monitoring by rest api with python script

The Python script and the Zabbix template in this repo allow you to monitor a 3CX Server by rest api.

Tested with Zabbix Version 6.0 on Ubuntu Server 20.04 LTS and 3CX Server 18.


## Setup

1. Connect to your Zabbix Server over ssh.
2. Run the following install command (installs python 3.9 and all required dependencies and copies all files):

``` shell
sudo apt update && sudo apt install git -y &&
git clone https://github.com/Noahnc/zabbix_3cx_monitoring.git &&
sudo chmod +x zabbix_3cx_monitoring/install.sh &&
sudo ./zabbix_3cx_monitoring/install.sh
```
3. Test if the scrip works.

Script-Check
``` shell
./usr/lib/zabbix/externalscripts/monitoring_3cx.py -u '<username>' -p '<password>' -d '<3cx domain>' --tcpport 443 -c "script-health-check" --debug True
```

3CX Trunks as JSON
``` shell
./usr/lib/zabbix/externalscripts/monitoring_3cx.py -u '<username>' -p '<password>' -d '<3cx domain>' --tcpport 443 -c "3cx-trunks" --debug True
```

4. Import the zabbix template.
5. Create a new host with the template and specify the required variables


