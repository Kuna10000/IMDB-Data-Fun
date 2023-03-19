# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 18:43:45 2023

@author: kurt
"""

from requests import get
from bs4      import BeautifulSoup as soup
import pandas as pd

def loadData(i,movotv):
    #load clicking the title bringing more movie/tv information
    moreInfoUrl = i.find('span',{'class':'lister-item-index unbold text-primary'}).find_next('a')['href']
    url         = get("https://www.imdb.com/"+moreInfoUrl,headers=headers).text
    nextPage    = soup(url,'html.parser')
    
    #load the dataId primary key
    dataId.append(currentId)
    
    #Start loading data----------------------------------------------------------------------------------
    
    #find the title
    try :
        titles.append(i.h3.a.text)
    except :
        titles.append("null")
    
    #find content type
    try :
        if movotv == "movie":
            contentType.append("movie")
        else :
            contentType.append("tvSeries")
    except:
        contentType.append("null")
        
    #find length/time
    try :
        time.append((i.p.find('span',{'class':'runtime'}).text).split(' ',1)[0])
    except:
        time.append(-1)
        
    #find year
    try:
        #Retrieve the listed year
        foundYear = (i.h3.find('span',{'class':'lister-item-year text-muted unbold'}).text).replace('(','').replace(')','').replace('I','')
        #if movie, send as is
        if movotv == "movie":
            startYear.append(int(foundYear))
            endYear.append(-1)
        #if tv show, we need to split 1994-1000 string, into start and end date
        else:
            fixedYear = foundYear.split("–")
            startYear.append(int(fixedYear[0]))
            if len(fixedYear) == 1:
                endYear.append(-1)
            elif fixedYear[1] == " ":
                endYear.append(-1)
            else :
                endYear.append(fixedYear[1])
    except:
        startYear.append(-1)
        endYear.append(-1)
        
    #find genres
    try:
        genreRaw = (i.p.find('span',{'class':'genre'}).text).replace(' ','')[1:]
        genreList = genreRaw.split(",")
        genre.append(genreList)
    except:
        genre.append("null")
        
    #find description
    try:
        description.append(i.findAll('p',{'class':'text-muted'})[1].text[1:].replace("See full summary",""))   
    except:
        description.append("null")
        
    #find rating
    try:
        rating.append(i.find('div',{'class':'ratings-bar'}).div.strong.text)
    except:
        rating.append(-1)
        
    #find amount of people who rated it
    try:
        votes.append(i.find('p',{'class':'sort-num_votes-visible'}).find_next('span').find_next('span').text.replace(',',''))
    except:
        votes.append(-1)
    
    #find the gross earned
    try :
        if movotv == "movie":
            grossVal = (i.find('p',{'class':'sort-num_votes-visible'}).findAll('span',{'name':'nv'})[1].text).replace('$','')
            newstr = ''
            if('M' in grossVal):
                s = grossVal.split('.')
                s[1] = s[1].replace('M','0000')
                newstr = s[0]+s[1]
            gross.append(newstr)
        else :
            gross.append(-1)
    except:
        gross.append(-1)
        
    #find the regions
    try :
        #need to reformat regions into a list of strings
        regsNoFilter = nextPage.find('li',attrs={'data-testid':'title-details-origin'}).findAll('li',attrs={'role':'presentation'})
        tempReg = []
        for reg in regsNoFilter:
            tempReg.append(reg.find_next('a').text)
        region.append(tempReg)
    except:
        region.append("null")
        
    #try get the certificate rating
    try :
        certificate.append(i.find('span',attrs={'class':'certificate'}).text)
    except : 
        certificate.append("null")
        

#package data into csv format
def packageData():
    
    rows             = list(zip(dataId,contentType,titles,time,startYear,endYear,votes,rating,gross,certificate,description))
    contentDataPrime = pd.DataFrame(rows,columns=['dataId','contentType','title','length','releaseYear','endYear','votes','rating','gross','certificate','description'])

    zipped           = list(zip(dataId, genre))
    genre_tuples     = [[dataId, genre] for dataId, genre_list in zipped for genre in genre_list]
    contentDataGenre =  pd.DataFrame(genre_tuples,columns=['dataId','genre'])

    zipped           = list(zip(dataId, region))
    genre_tuples     = [[dataId, region] for dataId, region_list in zipped for region in region_list]
    contentDataRegion= pd.DataFrame(genre_tuples,columns=['dataId','region'])

    try :
        dfp = pd.read_csv('C:/Users/kurt/OneDrive/CSV Files/imdb/contentDataPrime.csv')
        dfg = pd.read_csv('C:/Users/kurt/OneDrive/CSV Files/imdb/contentDataGenre.csv')
        dfr = pd.read_csv('C:/Users/kurt/OneDrive/CSV Files/imdb/contentDataRegion.csv')
        contentDataPrime = pd.concat([contentDataPrime,dfp])
        contentDataGenre = pd.concat([contentDataGenre,dfg])
        contentDataRegion= pd.concat([contentDataRegion,dfr])
        dataId.clear()
        titles.clear()     
        contentType.clear() 
        time.clear()     
        startYear.clear() 
        endYear.clear()    
        genre.clear()       
        votes.clear()     
        rating.clear()    
        gross.clear()      
        description.clear() 
        region.clear()     
        certificate.clear()
        currentId.clear()  
    except:
        pass
    
    contentDataPrime.to_csv('C:/Users/kurt/OneDrive/CSV Files/imdb/contentDataPrime.csv',index=False)
    contentDataGenre.to_csv('C:/Users/kurt/OneDrive/CSV Files/imdb/contentDataGenre.csv',index=False)
    contentDataRegion.to_csv('C:/Users/kurt/OneDrive/CSV Files/imdb/contentDataRegion.csv',index=False)
    

#needed to get through IMDB scraping resistance
headers     = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}

#data to collect
dataId      = [] #primary key
titles      = [] #title of movie or tv show
contentType = [] #Movie/Tv-Series
time        = [] #length of movie. length of an episode
startYear   = [] #will hold movie release year
endYear     = [] #will be null if movie
genre       = [] #genre
votes       = [] #amount of people who rated it
rating      = [] #the average rating
gross       = [] #gross earned
description = [] #descruption
region      = [] #regions its in
certificate = [] #maturity rating
currentId   = 0  #stores the place we are in the lists


url      = get("https://www.imdb.com/search/title/?title_type=feature,tv_movie,documentary,short&num_votes=100,&sort=num_votes,desc&count=250&start=001&ref_=adv_nxt",headers=headers).text
moviesMainPage = soup(url,'html.parser')
movies   = moviesMainPage.findAll('div',{'class':'lister-item mode-advanced'})

url      = get("https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&num_votes=100,&sort=num_votes,desc&count=250&start=001&ref_=adv_nxt",headers=headers).text
tvMainPage = soup(url,'html.parser')
tvSeries = tvMainPage.findAll('div',{'class':'lister-item mode-advanced'})

currentlyStored = []
try :
    dfp = pd.read_csv('C:/Users/kurt/OneDrive/CSV Files/imdb/contentDataPrime.csv')
    currentlyStored = list(dfp['title'])
except:
    pass


#590
for pageCount in range(590):
    
    if pageCount != 0:
        nextPageUrl = moviesMainPage.find('div',{'class':'desc'}).find('a',attrs={'class':'lister-page-next next-page'})['href']
        url      = get("https://www.imdb.com/"+nextPageUrl,headers=headers).text
        moviesMainPage = soup(url,'html.parser')
        movies   = moviesMainPage.findAll('div',{'class':'lister-item mode-advanced'})

    #load movies
    for a in movies:
        if a.h3.a.text not in currentlyStored:
            loadData(a,"movie")
        if currentId % 499 == 0:    
            if a.h3.a.text not in currentlyStored: 
                packageData()
            print("Fin ID",currentId)
        currentId += 1
#119     
    if pageCount <= 119:     
        if pageCount != 0:
            nextPageUrl = tvMainPage.find('div',{'class':'desc'}).find('a',attrs={'class':'lister-page-next next-page'})['href']
            url      = get("https://www.imdb.com/"+nextPageUrl,headers=headers).text
            tvMainPage = soup(url,'html.parser')
            tvSeries = tvMainPage.findAll('div',{'class':'lister-item mode-advanced'})        
                
        #load tvseries
        for b in tvSeries:
            if b.h3.a.text not in currentlyStored:
                loadData(b,"tvSeries")
            if currentId % 499 == 0:   
                if b.h3.a.text not in currentlyStored: 
                    packageData()
                print("Fin ID",currentId)    
            currentId += 1    
        
packageData()
            