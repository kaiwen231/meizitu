#coding=utf-8
import requests
from lxml import html
import os
import time

def getPage(url):
    print(url)
    print(requests.get(url).status_code)
    selector=html.fromstring(requests.get(url).content)
    urls = []
    for i in selector.xpath('//ul[@id="pins"]/li/a/@href'):
        urls.append(i)
    return urls


def getPicLink(url):
    # print(pic_url)
    # print(requests.get(pic_url).status_code)
    sel = html.fromstring(requests.get(url).content)
    title=sel.xpath('//h2[@class="main-title"]/text()')[0]
    if r':' in title:
        title=title.split(':')[1]
    print title
    page_num=sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    imgs = []
    for i in range(int(page_num)):
        page_url= url + '/' + str(i+1)
        print(page_url)
        print(requests.get(page_url).status_code)
        s = html.fromstring(requests.get(page_url).content)
        img_url=s.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
        time.sleep(1)
        print img_url
        imgs.append(img_url)
    return title,imgs

def getHeader(img_url):
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1515137765; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1515137765',
        'Host':'i.meizitu.net',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Referer':'%s' %img_url,
    }
    return headers


def downloadPic(title,imgs):
    file_path=r'meizitu/' + title
    print file_path
    os.mkdir(file_path)
    k=1
    for i in imgs:
        file_name= '/%d.jpg' %k
        with open(file_path+file_name,'wb') as jpg:
            jpg.write(requests.get(i,headers=getHeader(i)).content)
        k+=1

if __name__=='__main__':
    url='http://www.mzitu.com'
    pic_urls=getPage(url)
    #os.mkdir('meizitu')
    for pic_url in pic_urls:
        if pic_urls.index(pic_url)<20:
            continue
        pic_title,pic_imgs=getPicLink(pic_url)
        downloadPic(pic_title,pic_imgs)