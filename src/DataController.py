import json
import requests
from api_models.services import welcome_from_dict_services
from api_models.system_status import welcome_from_dict_systemstatus
import os
import time

class data_handler:
    base_url_3cx = ""
    username = ""
    password = ""
    chacheFolderPath = ""
    chacheTimeInSeconds = 0
    api = None


    def setup(self, api, time):
        self.api = api
        self.chacheTimeInSeconds = time 
        self.chacheFolderPath = "data_cache/" + api.domain

    def get3CXServices(self):
        CacheFileName = "3CXServices.json"
        response = self.api.get3CXServices()
        if self.checkIfFileIsOlderThan(CacheFileName, self.chacheTimeInSeconds):
            self.saveResponseToCache(response, CacheFileName)
            service = welcome_from_dict_services(json.loads(response))
        else:
            service = welcome_from_dict_services(self.loadResponseFromCache(CacheFileName))
        return service

    def get3CXServiceStatusByName(self, name):
        services = self.get3CXServices()
        for service in services:
            if service.name == name:
                return service.status

    def get3CXSystemStatus(self):
        CacheFileName = "3CXSystemStatus.json"
        response = self.api.get3CXSystemStatus()
        if self.checkIfFileIsOlderThan(CacheFileName, self.chacheTimeInSeconds):
            self.saveResponseToCache(response, CacheFileName)
            status = welcome_from_dict_systemstatus(json.loads(response))
        else:
            status = welcome_from_dict_systemstatus(self.loadResponseFromCache(CacheFileName))
        return status

    def saveResponseToCache(self, response, filename):
        self.checkIfFolderExists()
        with open(self.chacheFolderPath + "/" + filename, 'w') as outfile:
            json.dump(json.loads(response), outfile)

    def loadResponseFromCache(self, filename):
        with open(self.chacheFolderPath + '/' + filename, 'r') as outfile:
            return json.load(outfile)
    
    # create a function that takes a filename and a time in seconds and returns true if the file is older than the given time
    def checkIfFileIsOlderThan(self, filename, modifiedTime):
        if os.path.isfile(self.chacheFolderPath + '/' + filename):
            file_time = os.path.getmtime(self.chacheFolderPath + '/' + filename)
            if modifiedTime < (time.time() - file_time):
                return True
            else:
                return False
        else:
            return True

    def checkIfCacheFileExists(self, filename):
        return os.path.isfile(self.chacheFolderPath + '/' + filename)

    def checkIfFolderExists(self):
        if not os.path.exists(self.chacheFolderPath):
            os.mkdir(self.chacheFolderPath)


class api_handler:

    session = requests.Session()

    def __init__(self, user, pw, url):
        self.username = user
        self.password = pw
        self.base_url_3cx = "https://" + str(url) + "/api/"
        self.domain = url

    def getAccessCookie(self):
        url = self.base_url_3cx + 'login'
        payload = {'username': self.username, 'password': self.password}
        headers = {'content-type': 'application/json'}
        response = self.session.post(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        if response.status_code == 200 and response.text == 'AuthSuccess':
            cookie = response.cookies
            return cookie.get_dict()
        else :
            print("Authentication error, wrong username or password: " + response.text)
            return None

    def get3CXServices(self):
        url = self.base_url_3cx + 'ServiceList'
        headers = {'content-type': 'application/json;charset=UTF-8'}
        response = self.session.get(url, headers=headers, cookies=self.getAccessCookie())
        return response.text


    def get3CXSystemStatus(self):
        url = self.base_url_3cx + 'SystemStatus'
        headers = {'content-type': 'application/json;charset=UTF-8'}
        response = self.session.get(url, headers=headers, cookies=self.getAccessCookie())
        return response.text






