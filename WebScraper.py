# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 18:43:45 2023

@author: kurt
"""

from requests import get
from bs4 import BeautifulSoup as soup
import pandas as pd
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}

regList = ['us','ru','kr','fr','in','id','de','th','vn','CN']

for reg in regList: 

    url = get("https://www.imdb.com/search/title/?title_type=feature,documentary,short&countries="+reg+"&sort=num_votes,desc&count=100").text
    mainPage = soup(url,'html.parser')
    movies = mainPage.findAll('div',{'class':'lister-item mode-advanced'})
    
    titles = []
    time = []
    year = []
    genre = []
    votes = []
    rating = []
    gross = []
    description = []
    
    for x in range(1,50):
        for i in movies:
            titles.append(i.h3.a.text)
            try :
                time.append((i.p.find('span',{'class':'runtime'}).text).split(' ',1)[0])
            except:
                time.append(-1)
            try:
                year.append((i.h3.find('span',{'class':'lister-item-year text-muted unbold'}).text).replace('(','').replace(')',''))
            except:
                year.append(-1)
            try:
                genre.append((i.p.find('span',{'class':'genre'}).text).replace(' ','')[1:])
            except:
                genre.append(-1)
            try:
                description.append(i.findAll('p',{'class':'text-muted'})[1].text[1:])    
            except:
                description.append(-1)
            try:
                rating.append(i.find('div',{'class':'ratings-bar'}).div.strong.text)
            except:
                rating.append(-1)
            try:
                votes.append(i.find('p',{'class':'sort-num_votes-visible'}).find_next('span').find_next('span').text.replace(',',''))
            except:
                votes.append(-1)
            try :
                grossVal = (i.find('p',{'class':'sort-num_votes-visible'}).findAll('span',{'name':'nv'})[1].text).replace('$','')
                newstr = ''
                if('M' in grossVal):
                    s = grossVal.split('.')
                    s[1] = s[1].replace('M','0000')
                    newstr = s[0]+s[1]
                gross.append(newstr)
            except:
                gross.append(-1)
        
        #nextPage = mainPage.find('div',{'class':'desc'}).find_next('a')['href']
        #nextPage = "/search/title/?title_type=feature,documentary,short&languages=ja&count=100&start="+str(x)+"01&ref_=adv_nxt"
        nextPage = "/search/title/?title_type=feature,documentary,short&countries="+reg+"&sort=num_votes,desc&count=100&start="+str(x)+"01&ref_=adv_nxt"
        print(nextPage)
        nextPage = get("https://www.imdb.com"+nextPage,headers=headers).text
        
        nextPage = soup(nextPage,'html.parser')
        movies = nextPage.findAll('div',{'class':'lister-item mode-advanced'})
        
    
    rows=list(zip(titles,time,year,genre,votes,rating,gross,description))
    df = pd.DataFrame(rows,columns=['title','length(minutes)','year','genre','votes','rating','gross','description'])
    print(df)
    
    print(titles,time,year,genre,votes,rating,gross,description)
    
    df.to_csv('C:/Users/kurt/OneDrive/CSV Files/imdb/imdb_'+reg+'.csv',index=False)
    
