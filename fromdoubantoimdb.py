# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 18:57:43 2018

@author: hongwei.fhw
"""
#从豆瓣排名前250的电影分别链接到IMDB找出其评分和票房，但这个程序还有问题
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def get_imdbmovies():
    headersdouban = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
    'Host': 'movie.douban.com'
    }
    headersimdb ={
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
    'Host': 'www.imdb.com'
    }
    point_list=[]
    currency_list=[]
    gross_list=[]
    movie_list=[]
    
    #for i in range(0,10):
    for i in range(0,10):
        link = 'https://movie.douban.com/top250?start=' + str(i * 25)
        r = requests.get(link, headers=headersdouban, timeout= 1000)
        temp=r.text
        douban_rawlist = re.findall('https://movie.douban.com/subject/.*?/',temp)
        douban_list=[]
        [douban_list.append(i) for i in douban_rawlist if not i in douban_list]
        #print(type(douban_list[1]))
        soup = BeautifulSoup(r.text, "lxml")
        div_list1 = soup.find_all('div', class_='hd')#movie titles
        for each in div_list1:
            movie = each.a.span.text.strip()
            movie_list.append(movie)
            
        for j in range(len(douban_list)):
            print(i,j)
            doubansublink=douban_list[j]
            rr = requests.get(doubansublink, headers=headersdouban, timeout= 1000).content
            soup1 = BeautifulSoup(rr, "html.parser")
            tempbase=re.compile('http://www.imdb.com/title/tt\d{7}')#找出豆瓣上该电影对应的IMDB链接
            tempurl=re.findall(tempbase,str(soup1))
            print(tempurl[0])

            #print(rrr)
            if len(tempurl)==0:
                point=['None']
                currency=['None']
                netfee=['None']
            else:
                rrr = requests.get(tempurl[0], headers=headersimdb, timeout= 1000).content
                soup2 = BeautifulSoup(rrr, "html.parser")
                #tempbase2=re.compile('Gross USA:</h4> (.*?)\n')
                #tempgross=re.findall(tempbase2,str(soup2))
                tempbase2=re.compile('Gross USA:</h4> (.*?), <span')
                tempgross=re.findall(tempbase2,str(soup2))
                #pointcompile=re.compile('<span class="rating">(.*?)<span')
                pointcompile=re.compile('<span class="rating">\d{1}(\.\d{1})?')
                point=re.findall(pointcompile,str(soup2))
            #print(len(tempgross))
            #print(type(tempgross))
            if len(tempgross)==0:
                point=['None']
                currency=['None']
                netfee=['None']
            else:
                currency=tempgross[0][0]#每部电影总票房的货币种类
                netfeeelement=list(filter(str.isdigit,tempgross[0]))
                netfee=''.join(netfeeelement)#去掉逗号，将gross票房合成为一个值
#                pointcompile=re.compile('<span class="rating">(.*?)<span')
#                point=re.findall(pointcompile,str(soup2))
                #point=soup2.find_all('span', itemprop_='ratingValue')#找出每部电影的评分
            
            gross_list.append(netfee)
            currency_list.append(currency)
            point_list.append(point)

    mytemp={'1title': movie_list, '2imdbpoint': point_list, '3currency': currency_list, '4grossUSA': gross_list}
    myexcel=pd.DataFrame(mytemp)
    myexcel.to_csv('D:\Winpy\imdbpoint.csv',encoding='utf_8_sig')
    return point_list,currency_list,gross_list