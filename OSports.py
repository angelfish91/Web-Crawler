# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import urllib
import urllib2
import re
import time
from bs4 import BeautifulSoup


'''
written by sparrow
usage:
    
    a = grubOSports(n = 100, out_path = /path/to/your/dir)
    a.src_url = base_url
    a.main()
    
'''

class grubOSports(object):
    def __init__(self, n=10, out_path = r'D:\project\web_crawler\imgs-osports'):
        self.src_url = u"http://people.osports.com.cn/?id=6&page="
        self.grub_urls = []
        self.out_path = out_path
        for i in range(n):
            self.grub_urls.append(self.src_url+str(i+1))
        print self.out_path
    
    def getHtml(self, url):
        flag = 1
        while flag == 1:
            try:
                request = urllib2.Request(url)
                webfile = urllib2.urlopen(request)
                outhtml = webfile.read()
                flag = 0
            except urllib2.URLError:
                time.sleep(2)
                print 'Error Please check the network connection!!'
        return outhtml
           
    def parse(self, html):
        soup = BeautifulSoup(html, 'lxml')
        souplist = soup.select('a')
        links = []
        for i in souplist:
            if i.img!=None:
                try:
                    i.img['style']
                except:
                    try:
                        i.img['height']
                    except:
                        links.append(r'http://people.osports.com.cn/'+i['href'])
        return links
    
    def parseImgurl(self, url):
        html = self.getHtml(url)
        soup = BeautifulSoup(html, 'lxml')
        img_url = []
        links = soup.select('a')
        for i in links:
            try:
                match = re.match(re.compile(r"^photo.+"), i['href'])
                if match:
                    img_url.append( r'http://people.osports.com.cn/'+ match.group())
            except:
                pass
        return img_url
        
    def download(self, url, num, n,m):
        html = self.getHtml(url)
        soup = BeautifulSoup(html, 'lxml')
        imglist = []
        imgs = soup.select('img')
        for xx, i in enumerate(imgs):
            try:
                i['height']
                imglist.append(r'http://www.osports.cn/'+i['src'][2:])
                #print r'http://www.osports.cn'+i['src'][2:]
                filepathname = self.out_path+r'\\'+'000'+str(num)+r'_'+'000'+str(n)+'_'+'000'+str(m)+r'.jpg'
                
                urllib.urlretrieve(r'http://www.osports.cn'+i['src'][2:], 
                                   filepathname) 
                print filepathname
            except:
                pass
            
            
            
    def main(self):
        for num , url in enumerate(self.grub_urls):
            print '='*80
            print 'Global page:',num
            html = self.getHtml(url)
            links = self.parse(html)
            for n, i in enumerate(links):
                img_links = self.parseImgurl(i)
                for m, j in enumerate(img_links):
                    print 'Downloading from:', j
                    print 'Current page:',num+1, n+1, m+1
                    self.download(j,num,n,m)
        


def timelimit(timeout, func, args=(), kwargs={}):
    """ Run func with the given timeout. If func didn't finish running
        within the timeout, raise TimeLimitExpired
    """
    import threading
    class FuncThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            self.result = func(*args, **kwargs)

        def _stop(self):
            if self.isAlive():
                threading.Thread._Thread__stop(self)

    it = FuncThread()
    it.start()
    it.join(timeout)
    if it.isAlive():
        it._stop()
        raise IOError
    else:
        return it.result







