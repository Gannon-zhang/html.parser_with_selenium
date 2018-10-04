#coding=utf-8

from Page import _Page

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:(lineno)d]%(levelname)s %(message)s',datefmt='%a,%d %b %Y %H:%M:%S')

class _Page_List(object):
    def __init__(self):
        self.page_List = set()

    def update(self, objPage):
        if self.exist(objPage):
            logging.warn('{}[{}] has exist in Page_List!',format(objPage.handle,objPage.title))
        else:
            self.page_List.add(objPage)
            logging.info('{}[{}] add success!',format(objPage.handle,objPage.title))

    def remove(self, objPage):
        if self.exist(objPage):
            self.page_List.remove(objPage)
            logging.info('{}[{}] remove success!',format(objPage.handle,objPage.title))
        else:
            logging.warn('{}[{}] is not exist in Page_List!',format(objPage.handle,objPage.title))

    def exist(self,objPage):
        if objPage in self.page_List:
            return True
        else:
            return False


class BrowserError(Exception):
    pass


class Browser(object):
    def __init__(self, desired_capabilities = DesiredCapabilities.INTERNETEXPLORER):
        if desired_capabilities == DesiredCapabilities.INTERNETEXPLORER:
            self.__driver = webdriver.Ie()
        elif desired_capabilities == DesiredCapabilities.CHROME:
            self.__driver = webdriver.Chrome()
        elif desired_capabilities == DesiredCapabilities.FIREFOX:
            self.__driver = webdriver.Firefox()
        else:
            raise BrowserError('desired_capabilities error!')
        self.__init_Url = self.__driver.current_url
        self.__Page = _Page(self)
        self.__Page_List = _Page_List()
        self.__Page_List.update(self.__Page)


    @property
    def driver(self):
        return self.__driver

    @property
    def page(self):
        return self.__Page

    @property
    def page_List(self):
        return self.__Page_List

    def open(self, strUrl):
        pass