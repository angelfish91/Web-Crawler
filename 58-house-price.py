# -*- coding: utf-8 -*-
"""
Created on Thu Jul 06 06:18:45 2017

@author: 69390
"""


import os
import urllib
import urllib2
import re
import time
from bs4 import BeautifulSoup


import lxml.html as H  
from lxml.cssselect import CSSSelector



base_url = 'http://nj.58.com/chuzu/?PGTID=0d200001-000a-ce02-e77b-b4d16f8d1ab2&ClickID=1'
global PRICE
PRICE = []


def getHtml(url):
    flag = 1
    while flag == 1:
        try:
            request = urllib2.Request(url)
            webfile = urllib2.urlopen(request)
            outhtml = webfile.read()
            flag = 0
        except urllib2.URLError:
            print 'Error Please check the network connection!!'
            time.sleep(3)
            
    return outhtml   


def getPrice(html):
    doc = H.document_fromstring(html)
    count = 0
    for i in range(200):
        try:
            count += 1
            select_td = CSSSelector('body > div.mainbox > div.main > div.content > div.listBox > ul > li:nth-child(%d) > div.listliright > div.money > b' %(i+1))
            PRICE.append(select_td(doc)[0].text)
        except:
            print "Grub print num:", count
            break
                

def getNextPage(url):
    html = getHtml(url)
    getPrice(html)
    soup = BeautifulSoup(html, 'lxml')
    try:
        leaf = soup.select('#bottom_ad_li > div.pager > a.next')
        nextpage = leaf[0]['href']
        print 'Finding next parsing:',nextpage
    except:
        nextpage = None
    return nextpage



def main(url):
    page = 0
    flag = 1
    
    while flag == 1:
        page+=1
        print 'Parsing page:',page
        url = getNextPage(url)
        if url == None:
            flag = 0
        
    
if __name__ == '__main__':
    main(base_url)

     
