from abc import ABC, abstractmethod
import json
import os
import requests
from pathlib import Path
from ..Config.Config import Config
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

'''
    Scraper abstract class
'''

class Scraper:
    def __init__(self, url) -> None:
        self.url = url

    def __getResponse(self, isDynamic=False):
        # Because request only makes http request calls, change our https link to http
        protocol, link = self.url.split(':')
        if not isDynamic:
            protocol = 'http'
        else:
            protocol = 'https'
        url = protocol + ':' + link
        proxy = Config().get_proxy()
        if not isDynamic:
            response = requests.get(url,proxies = proxy,verify = False)
        else:
            os.environ["PATH"] += os.pathsep + os.getcwd().split("src",1)[0]
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            response = driver.page_source
            
        return response

    @abstractmethod
    def get_problem(self):
        pass