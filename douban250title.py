# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 15:42:40 2018

@author: hongwei.fhw
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def get_movies():
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
    'Host': 'movie.douban.com'
    }
    movie_list = []#movie name
    point_list = []#score of each movie
    commt_list = []#how many people commentted
    years_list = []#year of each movie
    other_list = []#comments of each movie
    for i in range(0,10):
        link = 'https://movie.douban.com/top250?start=' + str(i * 25)
        r = requests.get(link, headers=headers, timeout= 10)
        temp=r.text
        #print (str(i+1),"页响应状态码:", r.status_code)        
        soup = BeautifulSoup(r.text, "lxml")

        div_list1 = soup.find_all('div', class_='hd')#movie titles
        for each in div_list1:
            movie = each.a.span.text.strip()
            movie_list.append(movie)
            
        div_list2 = soup.find_all('span', class_='rating_num')#movie scores
        for each in div_list2:
            point = each.text.strip()
            point_list.append(point)
        
#        div_list3 = soup.find_all('div', class_='star')
#        for each in div_list3:
#            commt = each.span.text.strip()
#            commt_list.append(commt)
        div_list3 = re.findall('<span>.*?人评价</span>',temp)#viewer numbers 找出有comment数的行，然后找出有几个数字，然后把数字截取出来
        for ii in range(len(div_list3)):
            str1=list(filter(str.isdigit,div_list3[ii]))
            str2=len(str1)
            str3=div_list3[ii][6:6+str2]
            commt_list.append(str3)
        
        div_list4 = soup.find_all('p', class_='')#moive year
        for each in div_list4:
            year = each.text.strip()
            yeardig=list(filter(str.isdigit,year))
            netfee=''.join(yeardig)
            years_list.append(netfee)
            other_list.append(year)
        

            
        #print(type(div_list3))
        #div_list3 = re.findall('人评价$',temp)
        #div_list3 = div_list3.encode('gbk')
        #div_list3 = filter(str.isdigit,div_list3)
        #commt_list.append(div_list3)

    mytemp={'1title': movie_list, '2point': point_list, '3viewers': commt_list, '4years': years_list, '5comments':other_list}
    myexcel=pd.DataFrame(mytemp)
    myexcel.to_csv('D:\Winpy\doubanrank.csv',encoding='utf_8_sig')
    return movie_list,point_list,commt_list


    
    
#movies = get_movies()
#print(movie_list)

