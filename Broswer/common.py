#coding=utf-8
import base64
import logging
import ConfigParser
import os
import time
import re
import threading
import subprocess
from multiprocessing import Pool

from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException

from Tools import *

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:(lineno)d]%(levelname)s %(message)s',datefmt='%a,%d %b %Y %H:%M:%S',filename='logging.log',filemode='w')

class Broswer():
    def __init__(self,strUrl,strBroswer='Chrome'):
        paraLegalityCheck({str:strUrl,str:strBroswer})
        if strBroswer == 'IE':
            self._driver = webdriver.Ie()
        elif strBroswer == 'Chrome':
            self._driver = webdriver.Chrome()
        elif strBroswer == 'Chrome_headless':
            opt = webdriver.ChromeOptions()
            opt.set_headless()
            self.opt.set_headless()
            self._driver = webdriver.Chrome(options=opt)
        elif strBroswer == 'FireFox':
            self._driver = webdriver.Firefox()
        elif strBroswer == 'Edge':
            self._driver = webdriver.Edge()
        elif strBroswer == 'Opera':
            self._driver = webdriver.Opera()
        elif strBroswer == 'Safari':
            self._driver = webdriver.Safari()
        else:
            raise Exception('{} is not supported.'.format(strBroswer))
        self.getIntoIframe = 0
        self._broswerType = strBroswer
        self._soup = None
        self._driver.get(strUrl)
        logging.info('broswer init success at {}'.format(time.ctime()))

    def CLick(self, by=By.ID,strValue='',strExec='selenium'):
        paraLegalityCheck({str:strValue,str:strValue})
        if strExec == 'js':
            if by == By.ID:
                js = re.sub(r'\\',r'',r"document.getElementById('{}').click()".format(strValue))
            elif by == By.CLASS_NAME:
                js = re.sub(r'\\', r'', r"document.getElementByClassName('{}').click()".format(strValue))
            elif by == By.NAME:
                js = re.sub(r'\\', r'', r"document.getElementByName('{}').click()".format(strValue))
            else:
                raise Exception('js just support ID、CLASS_NAME、NAME,not {}'.format(by))
        elif strExec == 'selenium':
            self._driver.find_element(by,strValue)
        elif strExec == 'mouse':
            ActionChains(self._driver).click((self._driver.find_element(by,strValue))).perform()
        else:
            raise Exception('para of strExec is error:{}.'.format(strExec))
        logging.info("click '{}' by '{}','{}' success.".format(strValue,by,strExec))

    def Loop_CLick(self,by = By.ID,strValue = '',strExec = 'selenium'):
        paraLegalityCheck({str:strExec,str:strValue})
        times = 0
        try:
            while self._driver.find_element(by,strValue):
                self.CLick(by,strValue,strExec)
                time.sleep(0.5)
                times += 1
        except:
            logging.info("click '{}' by '{}','{}' success,{} times.".format(strValue,by,strExec,times))

    def ExtraTable(self,by = None,strValue = None):
        paraLegalityCheck({str:strValue})
        htmlSource = self.getHtmlSource()
        form_item = []
        baseTable = None
        if by == None:
            baseTable = htmlSource.tbody.children
        else:
            baseTable = htmlSource.find(attrs={by:strValue}).children
        if baseTable == None:
            raise Exception('Do not get the table.')
        for tr in baseTable:
            form_tr = []
            if str(type(tr)) == '<class bs4.element.NavigableString>':
                return tuple(form_item)
            for td in tr.children:
                if td.text == u'\n':
                    form_tr.append('')
                elif td.text.encode('utf-8')[-1] == '\n':
                    form_tr.append(td.text.encode('utf-8')[0:-1])
                else:
                    form_tr.append(td.text.encode('utf-8'))
            form_item.append(tuple(form_tr))
        return form_item

    def getHtmlSource(self,*args):
        htmlFileName = re.sub(' ','_',self._driver.title.encode('utf-8')+str(time.ctime())+'.html')
        htmlFIlePath = '.\\htmlSource'
        html_file = open(os.path.join(os.getcwd(),os.path.join(htmlFileName,htmlFIlePath)),'w')
        self._soup = BeautifulSoup(self._driver.page_source,'html.parser')
        isFailed = 1
        if args:
            if self.getIntoIframe:
                for item in self._soup.find_all('iframe'):
                    try:
                        if item.attrs['id'].encode('utf-8') == args:
                            self._driver.switch_to_frame(args)
                            logging.info('get into {} iframe success.'.format(args))
                            self._soup = BeautifulSoup(self._driver.page_source,'html.parser')
                            isFailed = 0
                            break
                    except:
                        pass
        if isFailed:
            raise Exception('get into {} iframe failed'.format(args))
        html_file.write(str(self._soup))
        html_file.close()

    def getPrevious_sibling(self,tag):
        num = 1
        for i in list(tag.previous_siblings):
            if i.name == tag.name:
                num += 1
        return num

    def getXpath(self,tag):
        xpath = '/'+tag.name.encode('utf-8')
        for i in range(1000):
            tag = tag.parent
            xpath = '/'+tag.name.encode('utf-8')+'[%s]'%self.getPrevious_sibling(tag)+xpath
            if tag.name == u'html':
                break
        logging.info(xpath)
        return xpath

    def inputWrite(self,strName,strWords,strExec = 'selenium',iDepth = 2):
        paraLegalityCheck({str:strName,str:strWords,str:strExec,int:iDepth})
        isFailed = 1
        tag = None
        self.getHtmlSource()
        for i in self._soup.find_all('input'):
            tagTmp = i
            for item in range(iDepth):
                tagTmp = tagTmp.parent
                for j in tagTmp.children:
                    for k in j:
                        if strName in str(k):
                            logging.info('{} is found.'.format(strName))
                            tag = i
                            isFailed = 0
                            break
                    if isFailed == 0:
                        break
                if isFailed == 0:
                    break
            if isFailed == 0:
                break
        if isFailed:
            raise Exception('{} is not found.'.format(strName))
        if strExec == 'selenium':
            self._driver.find_element_by_xpath(self.getXpath(tag)).clear()
            self._driver.find_element_by_xpath(self.getXpath(tag)).send_keys(strWords)
        elif strExec == 'js':
            js = "document.getElementById('{}').value = {}".format(tag.attrs['id'].encode('utf-8'),strWords)
            self._driver.execute_script(js)
        else:
            raise Exception('strExec is error:{}'.format(strExec))
        logging.info("words '{}' has wrote in {} by {}".format(strWords,strName,strExec))





if __name__ == '__main__':
    logging.info('123')