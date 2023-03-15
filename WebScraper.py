# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 18:43:45 2023

@author: kurt
"""

from requests import get
from bs4      import BeautifulSoup as soup
import pandas as pd

headers  = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
url      = get("https://www.imdb.com/search/title/?title_type=feature,tv_movie,tv_series,documentary,short&num_votes=100,&count=10,&sort=num_votes,desc").text
mainPage = soup(url,'html.parser')
movies   = mainPage.findAll('div',{'class':'lister-item mode-advanced'})

movieId = []
titles = []
time = []
year = []
genre = []
votes = []
rating = []
gross = []
description = []
region = []

currentId = 0

for i in movies:
    movieId.append(currentId)
    try :
        titles.append(i.h3.a.text)
    except :
        titles.append(-1)
    try :
        time.append((i.p.find('span',{'class':'runtime'}).text).split(' ',1)[0])
    except:
        time.append(-1)
    try:
        year.append((i.h3.find('span',{'class':'lister-item-year text-muted unbold'}).text).replace('(','').replace(')',''))
    except:
        year.append(-1)
    try:
        genreRaw = (i.p.find('span',{'class':'genre'}).text).replace(' ','')[1:]
        genreList = genreRaw.split(",")
        genre.append(genreList)
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
    try :
        nextPageUrl = i.find('span',{'class':'lister-item-index unbold text-primary'}).find_next('a')['href']
        url = get("https://www.imdb.com/"+nextPageUrl,headers=headers).text
        nextPage = soup(url,'html.parser')
        regsNoFilter = nextPage.find('li',attrs={'data-testid':'title-details-origin'}).findAll('li',attrs={'role':'presentation'})
        tempReg = []
        for reg in regsNoFilter:
            tempReg.append(reg.find_next('a').text)
        region.append(tempReg)
    except:
        region.append(-1)
    
    if currentId <= 20:
        print("Fin ID",currentId)
    elif currentId % 10 == 0 and currentId <= 500:    
        print("Fin ID",currentId)
    elif currentId % 100 == 0:    
        print("Fin ID",currentId)
        
    currentId += 1
    

    

#nextPage = mainPage.find('div',{'class':'desc'}).find_next('a')['href']
#nextPage = "/search/title/?title_type=feature,documentary,short&languages=ja&count=100&start="+str(x)+"01&ref_=adv_nxt"
#nextPage = "/search/title/?title_type=feature,documentary,short&countries="+reg+"&sort=num_votes,desc&count=100&start="+str(x)+"01&ref_=adv_nxt"
#print(nextPage)
#nextPage = get("https://www.imdb.com"+nextPage,headers=headers).text

#nextPage = soup(nextPage,'html.parser')
#movies = nextPage.findAll('div',{'class':'lister-item mode-advanced'})



rows = list(zip(movieId,titles,time,year,votes,rating,gross,description))
movieDataPrime = pd.DataFrame(rows,columns=['movieId','title','length','releaseYear','votes','rating','gross','description'])

zipped = list(zip(movieId, genre))
genre_tuples = [[movieId, genre] for movieId, genre_list in zipped for genre in genre_list]
movieDataGenre =  pd.DataFrame(genre_tuples,columns=['movieId','genre'])

zipped = list(zip(movieId, region))
genre_tuples = [[movieId, region] for movieId, region_list in zipped for region in region_list]
movieDataRegion = pd.DataFrame(genre_tuples,columns=['movieId','region'])

print(movieDataGenre.head())

print(movieDataRegion.head())

print(movieDataPrime.head())

movieDataPrime.to_csv('C:/Users/kurt/OneDrive/CSV Files/imdb/movieDataPrime.csv',index=False)
movieDataGenre.to_csv('C:/Users/kurt/OneDrive/CSV Files/imdb/movieDataGenre.csv',index=False)
movieDataRegion.to_csv('C:/Users/kurt/OneDrive/CSV Files/imdb/movieDataRegion.csv',index=False)

    
