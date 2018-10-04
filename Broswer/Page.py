#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By

class PageError(Exception):
    pass

class _Page(object):
    '''
    page is object
    '''
    def __init__(self,objBrowser):
        self.__browser = objBrowser

    @property
    def browser(self):
        return self.__browser

    @property
    def driver(self):
        return self.browser.driver

    @property
    def title(self):
        return self.driver.title

    @property
    def page_source(self):
        return self.driver.page_source

    @property
    def handle(self):
        return self.driver.current_window_handle

    def execute_script(self,strScript):
        self.driver.execute_script(strScript)

    def find_element(self, by = By.ID, strValue = ''):
        self.driver.find_element(by, strValue)