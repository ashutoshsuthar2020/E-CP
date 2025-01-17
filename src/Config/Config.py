import json
import os
import requests
import click
from pathlib import Path
from ..Runner.exceptions.UnsupportedLanguage import UnsupportedLanguage
from .exceptions.UserNotFound import UsernameNotFound
from .exceptions.UserNotSet import UserNotSet
from requests.adapters import HTTPAdapter, Retry
'''
    Class to manage config related commands
'''
class Config():
    supported_lang = ['cpp', 'python', 'java']

    def __init__(self) -> None:
        self.config_file_path = self.get_config_path()

    def get_config_path(self) -> Path:
        config_file_path = Path(os.path.dirname(os.path.realpath(__file__)), 'config.json')
        return config_file_path

    def get_lang(self):
        config_file_path = self.config_file_path
    
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
        
        return config['language']

    def __is_lang_supported(self, lang):
        return lang in self.supported_lang

    def set_lang(self, lang):
        if(not self.__is_lang_supported(lang)):
            raise UnsupportedLanguage(lang)

        with open(self.config_file_path, 'r+') as config_file:
            config = json.load(config_file)
            config['language'] = lang
            config_file.seek(0)
            config_file.truncate()
            config_file.write(json.dumps(config))

    def set_template(self, temp_path):
        abs_path = os.path.abspath(temp_path)
        with open(self.config_file_path, 'r+') as config_file:
            config = json.load(config_file)
            config['template'] = abs_path
            config_file.seek(0)
            config_file.truncate()
            config_file.write(json.dumps(config))

    def get_template_path(self):
        config_file_path = self.config_file_path
    
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
        
        return config['template']

    def is_text_file(self, file_name):
        try:
            with open(file_name, 'tr') as check_file:
                check_file.read()
                return True
        except:
            return False

    def set_proxy(self, address):
        with open(self.config_file_path, 'r+') as config_file:
            config = json.load(config_file)
            config['proxy'] = address
            config_file.seek(0)
            config_file.truncate()
            config_file.write(json.dumps(config))

    def get_proxy(self):
        with open(self.config_file_path, 'r') as config_file:
            config = json.load(config_file)
        proxy =  config['proxy']
        if len(proxy)==0:
            proxy = {'http':'','https':''}
        else:
            proxy = {'http':'http://'+proxy}
        return proxy
    
    def remove_proxy(self):
        with open(self.config_file_path, 'r+') as config_file:
            config = json.load(config_file)
            config['proxy'] = ""
            config_file.seek(0)
            config_file.truncate()
            config_file.write(json.dumps(config))

    def set_user(self, user):
        api_url = "https://codeforces.com/api/user.info?handles="
        response = requests.get(url = api_url + user, proxies = self.get_proxy())
        if(response.status_code != 200):
            raise UsernameNotFound(user)
        html_content = response.json()
        config_file_path = self.config_file_path
        with open(config_file_path, 'r+') as config_file:
            config = json.load(config_file)
            config["user"]["firstname"] = html_content["result"][0]["firstName"]
            config["user"]["lastname"] = html_content["result"][0]["lastName"]
            config["user"]["rating"] = html_content["result"][0]["rating"]
            config["user"]["contri"] = html_content["result"][0]["contribution"]
            config["user"]["rank"] = html_content["result"][0]["rank"]
            config["user"]["maxrating"] = html_content["result"][0]["maxRating"]
            config_file.seek(0)
            config_file.truncate()
            config_file.write(json.dumps(config))

    def get_user(self):
        config_file_path = self.config_file_path
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
        if(len(config["user"]["firstname"]) == 0):
            raise UserNotSet()
        for info in config["user"]:
            print(info + " : " + str(config["user"][info]))
