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
    nextPageUrl = i.find('span',{'class':'lister-item-index unbold text-primary'}).find_next('a')['href']
    url         = get("https://www.imdb.com/"+nextPageUrl,headers=headers).text
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
        

#package data into csv format
def packageData():
    rows             = list(zip(dataId,contentType,titles,time,startYear,endYear,votes,rating,gross,description))
    contentDataPrime = pd.DataFrame(rows,columns=['dataId','contentType','title','length','releaseYear','endYear','votes','rating','gross','description'])

    zipped           = list(zip(dataId, genre))
    genre_tuples     = [[dataId, genre] for dataId, genre_list in zipped for genre in genre_list]
    contentDataGenre =  pd.DataFrame(genre_tuples,columns=['dataId','genre'])

    zipped           = list(zip(dataId, region))
    genre_tuples     = [[dataId, region] for dataId, region_list in zipped for region in region_list]
    contentDataRegion= pd.DataFrame(genre_tuples,columns=['dataId','region'])

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
currentId   = 0  #stores the place we are in the lists


for pageCount in range(99):
    url      = get("https://www.imdb.com/search/title/?title_type=feature,tv_movie,documentary,short&num_votes=100,&sort=num_votes,desc&count=100&start="+str(pageCount)+"01&ref_=adv_nxt",headers=headers).text
    mainPage = soup(url,'html.parser')
    movies   = mainPage.findAll('div',{'class':'lister-item mode-advanced'})
    
    #Get data/page for tv-series
    #url      = get("https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&num_votes=100,&sort=num_votes,desc").text
    url      = get("https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&num_votes=100,&sort=num_votes,desc&count=100&start="+str(pageCount)+"01&ref_=adv_nxt",headers=headers).text
    mainPage = soup(url,'html.parser')
    tvSeries = mainPage.findAll('div',{'class':'lister-item mode-advanced'})
    
    #load movies
    for a in movies:
        loadData(a,"movie")
        currentId += 1
        
        #for me to track output, make sure its still running after some crazy amount of data
        if currentId <= 20:
            print("Fin ID",currentId)
        elif currentId % 10 == 0 and currentId <= 500:    
            print("Fin ID",currentId)
        elif currentId % 500 == 0:    
            packageData()
            print("Fin ID",currentId)
            
    #load Tv shows
    for b in tvSeries:
        loadData(b,"tvSeries")
        currentId += 1
    
        #for me to track output, make sure its still running after some crazy amount of data
        if currentId <= 20:
            print("Fin ID",currentId)
        elif currentId % 10 == 0 and currentId <= 500:    
            print("Fin ID",currentId)
        elif currentId % 500 == 0:    
            packageData()
            print("Fin ID",currentId)
            
packageData()
    
