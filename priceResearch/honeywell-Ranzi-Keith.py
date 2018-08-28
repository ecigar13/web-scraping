# initial
import os
import json
import pandas as pd
from lxml.etree import HTML
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from bs4 import BeautifulSoup
import urllib
import requests
from requests.exceptions import HTTPError
import time
import os
import random
import sys


def readProductId():
    """return a panda frame"""
    types = pd.read_excel('Honeywell Obsolete Products.xlsx')
    types = types['Infrared Sensor Obsolescence - Affected Part Numbers']
    print(types[:5])
    return types


def buildLink(productNum):
    url = 'https://www.eciaauthorized.com/en/search/' + \
        productNum.encode('utf-8')
    print('url: {}'.format(url))
    return url


def getPage(url):
    """fetch website and raise error if it happens"""
    while True:
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                             )
            r.raise_for_status()
        except HTTPError as errh:
            print("Http Error:", errh)
            print(
                "It is likely that the program has reached the end of the story and is not an error.")
            self.closeFile()
            exit(0)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            print("Retrying in a few seconds.")
            time.sleep(5)
            continue
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            print("Retrying in a few seconds.")
            time.sleep(5)
            continue
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            self.writeToFile()
        else:
            return r


def writeToFile(dFrame):
    """write to file"""
    writer = pd.ExcelWriter('result.xlsx')
    dFrame.to_excel(writer, 'Sheet1')
    writer.save()


""" 
dcap = dict(DesiredCapabilities.CHROME)
dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')

# phantomjs deprecated. pls replace.
browser = webdriver.Chrome(executable_path=r'E:\py_wd\phantomjs-2.1.1-windows\bin\phantomjs.exe',
                             desired_capabilities = dcap, service_args = ['--ignore-ssl-errors=true'])
browser.implicitly_wait(10) """


def get_data(pn):
    url = 'https://www.eciaauthorized.com/en/search/'+pn.encode('utf-8')
    print('url: {}'.format(url))
    dt = pd.DataFrame()

    browser.get(url)
    html = HTML(browser.page_source)
    a = html.xpath('//script/text()')
    for i in range(len(a)):
        if 'SetCompletion' in a[i]:
            len1 = a[i].encode('utf-8').find('ExactResults')+16
            len2 = a[i].encode('utf-8').find('DistributorStatus')-12
            s = '{'+a[i].encode('utf-8')[len1:len2]+'}'
            d = json.loads(s)
            print('Name:{}'.format(d['Distributor']['DisplayName']))
            print('Prices:{}'.format(d['Prices']))
            print('')
            df = pd.DataFrame(d['Prices'], columns=[
                              'FormattedQuantity', 'FormattedPrice', 'Quantity'])
            if len(df) > 0:
                df['PartNumber'] = pn
                df['Distributior'] = d['Distributor']['DisplayName']
                dt.append(df, ignore_index=True)
    return dt


df = pd.DataFrame()
for pn in types:
    df.append(get_data(pn), ignore_index=True)
writer = pd.ExcelWriter('result.xlsx')
df.to_excel(writer, 'Sheet1')
writer.save()
