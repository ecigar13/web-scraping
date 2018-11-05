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
  """create the full url to put in browser"""
  url = 'https://www.eciaauthorized.com/en/search/' + productNum
  return url


def getPage(url):
  """fetch website and raise error if it happens"""
  while True:
    try:
      r = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'}
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
  """write to dataframe to file"""
  writer = pd.ExcelWriter('result.xlsx')
  dFrame.to_excel(writer, 'Sheet1')
  writer.save()


def get_data(pn):

  for i in range(len(a)):
    if 'SetCompletion' in a[i]:
      len1 = a[i].encode('utf-8').find('ExactResults') + 16
      len2 = a[i].encode('utf-8').find('DistributorStatus') - 12
      s = '{' + a[i].encode('utf-8')[len1:len2] + '}'
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


types = readProductId()
for pn in types:
  url =buildLink(pn)
  response = getPage(url)
  print(response.text)

print(type(types))
writeToFile(types)

