# IMDB-Data-Fun
Used python and the beautiful soup library to web scrape 28,000 tv shows and 73,000 movies data from the IMDB website. Used that data to make a visualization in PowerBi that allows the user to query for movies or tv shows based on region, genre, rating, etc and shows insights about the data.

### Files
- ContentDataPrime: Holds contents dataId (primary key), contentType, title, length, releaseYear, endYear, votes, rating, gross, certificate, description
- ContentDataRegion : Holds contents dataId (foreign key), region
- ContentDataGenre : Holds contents dataId (foreign key), genre
- WebScraper.py : IMDB webscraping script


### Purpose
My friends and I love cinema and are always looking for new things to watch. Finding movies in different genres and regions was always a difficult thing as well as finding something that was the right length of the day. IMDB offers a filter system in their search but we found it very difficult to quickly switch between regions, genres, etc.

The desire was for a fast way to query for movies or tvshows based on region, genre, length, rating, and more. 

### Getting The Data
Using the beautiful soup library in python, I was able to scrape the web data off these two links :
[Movies](https://www.imdb.com/search/title/?title_type=feature,tv_movie,documentary,short&num_votes=100,&sort=num_votes,desc&count=250&start=001&ref_=adv_nxt), [TvShows](https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&num_votes=100,&sort=num_votes,desc&count=250&start=001&ref_=adv_nxt)
Also uploaded to Kaggle : https://www.kaggle.com/datasets/kurtnakasato/imdb-100000-moviestvshows

- These pages returned 250 movies/tvshows per page. Each page was sorted in descending order of vote count (amount of people who rated it). This ensured that the content scraped will have some reputability in their rating. None of the contents scraped had a vote count under 100.

Here is a sample of the data format after scraping. 

<img width="264" alt="image" src="https://user-images.githubusercontent.com/113560906/229652629-ce2b9fc8-2b3a-459c-8a22-066df33a93b0.png"><img width="263" alt="image" src="https://user-images.githubusercontent.com/113560906/229652652-c9a0a993-6353-4a25-b716-90b3df1886e8.png">

<img width="1311" alt="image" src="https://user-images.githubusercontent.com/113560906/229652525-9b76a2d8-0433-4b3e-980b-2401b9a80ea6.png">

The data had -1 as missing number values and "null" as missing string values. missing values was made consistant in PowerBI to blank(). 
There were also some duplicate rows which was cleaned in PowerBI.

Here are some insights after cleaning the data.
<img width="700" alt="image" src="https://user-images.githubusercontent.com/113560906/229966305-20e26f07-fafe-4d71-b3d8-cd09a707dcd0.png">

___
### Displaying The Data
Used PowerBi to make a query tool for my friends and I to find movies/tvshows for movie night.

<img width="700" alt="image" src="https://user-images.githubusercontent.com/113560906/229659451-aed8f04e-0c64-4d22-bbbd-40e536f83de6.png">

### Results
The user is able to query for content based on many parameters in a fast way.
Here are some examples :

"I would like to watch a movie released in 1940 to 2000 from Iran."
<img width="700" alt="image" src="https://user-images.githubusercontent.com/113560906/229659183-77e700ac-9ff3-496b-a825-f26f42721ab8.png">

"I would like to watch anything that is a mystery and pg-13."
<img width="700" alt="image" src="https://user-images.githubusercontent.com/113560906/229659433-93736768-b722-491a-966c-560880844506.png">

"What region has the highest rated content?"
<img width="700" alt="image" src="https://user-images.githubusercontent.com/113560906/229657819-ec680db5-bc83-4c31-948d-10099b253a88.png">

___

### Challenges/Follow Up
- I didnt realize that TV-Movies had the release year in a different location than regular movies. Because of this, almost every TV-Movie is missing a release year leading to a very high missing movie release year percentage.
- The code for scraping was very slow and crashed often. Because of this, it took around 3 days of scraping before it finished 102k results. Although the code should skip duplicates already in the csv, it is still really slow which means refreshing the data with fresh data is unoptimal and unoften.

-Learning and implementing Multiprocessing in Python would be a very cool follow up to allow for faster scraping which means fresher data. 

-Changing the code to retrieve the missing release years on TV-Movies and other missing values would be great for further analysis and accuracy.

-Grabbing data from other data sources would also be great as the majority of the titles are USA based. The diffi


