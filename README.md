# IMDB-Data-Fun
Used python and the beautiful soup library to web scrape 28,000 tv shows and 73,000 movies data from the IMDB website. Used that data to make a visualization in PowerBi that allows the user to query for movies or tv shows based on region, genre, rating, etc and shows insights about the data.

### Purpose
My friends and I love cinema and are always looking for new things to watch. The common problem we would come across is finding a movie we want to watch. Finding movies of high value in different genres and regions was always a difficult thing to do for us as well as finding something that was the right length of the day. IMDB offers a filter system in their search but we found it very difficult to quickly switch between regions or genres etc.
The desire was for a fast way to query for movies or tvshows based on region, genre, length, and rating. 

### Developement
Using the beautiful soup library in python, I was able to scrape the web data off these two links :
https://www.imdb.com/search/title/?title_type=feature,tv_movie,documentary,short&num_votes=100,&sort=num_votes,desc&count=250&start=001&ref_=adv_nxt https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&num_votes=100,&sort=num_votes,desc&count=250&start=001&ref_=adv_nxt
These pages returned 250 entities per page. Each page was sorted in descending order of vote count (amount of people who rated it). This ensured that the entities scraped will have some reputability in their rating. None of the entities scraped had a vote count under 100.
The scraper simply went through each entity listed and logged its contents to a csv file after every page. After each page, it would move to the next untill it hit around 73k movies and 28k tvshows. 




