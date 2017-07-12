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

'''
written by sparrow
百度图片爬取程序，爬取的图片可以用于训练神经网络

使用方法：
1. 定义url，url为百度搜索分页模式的，注意一定要是分页模式下的网址
2. outpath为存储图片的地址
3. 如果出现：'Error Please check the network connection!!'， 请检查网络，
待网络连接正常，程序将继续爬取
'''
url = u"http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E5%AE%87%E5%AE%99%E5%9B%BE%E7%89%87&pn=0&gsm=64&ct=&ic=0&lm=-1&width=0&height=0"
#url = u"https://lvyou.baidu.com/zhongshanlingyinyuetai/fengjing/"
outpath = r"D:\project\web_crawler\imgs-space"

urls = []
urls_done = []


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


def init_urls (source, urllib):
    html = getHtml(source)
    url_list = getNextPage(html)
    mix = set(url_list)-set(urllib)
    for i in list(mix):
        urllib.append(i)
    return urllib

def update_urls (url, urls, urls_done):
    html = getHtml(url)
    url_list = getNextPage(html)
    mix = set(url_list)-(set(urls)|set(urls_done))
    for i in list(mix):
        urls.append(i)
    return urls

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
            
            
    #print outhtml
    return outhtml


def getNextPage(html):
    restr = ur'('
    restr += ur'\/search\/flip[^\s,"]*height=0'
    restr += ur')'    
    htmlurl = re.compile(restr)
    tem = re.findall(htmlurl, html)
    urlList = []
    for i in tem:       
        urlList.append(r'http://image.baidu.com'+i)   
    return urlList

def getImageList(html):
    restr = ur'('
    restr += ur'http:\/\/[^\s,"]*\.jpg'
#    restr += ur'|http:\/\/[^\s,"]*\.jpeg'
#    restr += ur'|http:\/\/[^\s,"]*\.png'
#    restr += ur'|http:\/\/[^\s,"]*\.gif'
#    restr += ur'|http:\/\/[^\s,"]*\.bmp'
#    restr += ur'|https:\/\/[^\s,"]*\.jpeg'
#    restr += ur'|https:\/\/[^\s,"]*\.jpeg'
#    restr += ur'|https:\/\/[^\s,"]*\.png'
#    restr += ur'|https:\/\/[^\s,"]*\.gif'
#    restr += ur'|https:\/\/[^\s,"]*\.bmp'
    restr += ur')'
    htmlurl = re.compile(restr)
    imgList = re.findall(htmlurl, html)
    print imgList
    return imgList

def download(imgList, page):
    x = 1
    for imgurl in imgList:
        try:
            filepathname = str(outpath +r'\\'+ 'pic_%09d_%010d' % (page, x) + str(
                os.path.splitext(urllib2.unquote(imgurl).decode('utf8').split('/')[-1])[1])).lower()
            print '[Debug] Download file :' + imgurl + ' >> ' + filepathname
            try:
                timelimit(10, urllib.urlretrieve,(imgurl, filepathname))
            except:
                print 'eception!'
        except:
            print 'fatial error!!!!!!!!'
        x += 1


def action(url,page):
 
    html = getHtml(url)
    imageList = getImageList(html)  
    download(imageList, page)
    return None


def downImageNum(url,urls,urls_done, n):
    urls = init_urls (url, urls)
    for i in range(n):
        exe_url = urls.pop(0)
        action(exe_url, i )
        urls_done.append(exe_url)
        try:
            urls = update_urls (exe_url, urls, urls_done)
            print len(urls), len(urls_done)
        except:
            pass
        print 'page:',i

if __name__ == '__main__':
    downImageNum(url, urls,urls_done, n = 200)








