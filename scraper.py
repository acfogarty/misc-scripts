import requests
import time
import sys
from bs4 import BeautifulSoup

#Usage:
#python scraper.py baseUrl firstPageUrl tagName className
#or
#python scraper.py baseUrl firstPageUrl tagName className loginUrl username password 

#gets text of all tags tagName of class className
#outputs text in plaintext file
#loops over many pages of search results, starting at firstPageUrl
#(code for getting url of next page of search results is not generalised, see TODO below)

#logs in first if login data is supplied

crawlDelay = 30 #seconds

baseUrl       = sys.argv[1] #base for relative links TODO get automatically
firstPageUrl  = sys.argv[2] #url to start scraping at
tagName       = sys.argv[3] #tag to search for
className     = sys.argv[4] #class to search for

#get login data if supplied
if len(sys.argv) > 5:
  loginUrl = sys.argv[2]
  payload  = {
    'user': sys.argv[3],
    'password': sys.argv[4],
  }
else:
  loginUrl = None

with requests.Session() as session:

  #start logged-in session if password was supplied
  if loginUrl:
    p = session.post(loginUrl, data=payload)

  #loop over pages
  print '#first page ',firstPageUrl
  nextPageUrl = firstPageUrl
  while (nextPageUrl):
    #read current page
    #print 'Reading page ',nextPageUrl
    response = requests.get(nextPageUrl)
    soup = BeautifulSoup(response.text)

    #get link to next page
    try:
      nextPageUrl = soup.find('a',{'rel':'next'}).get('href') #TODO generalise
      nextPageUrl = baseUrl + nextPageUrl
    except AttributeError:
      nextPageUrl = None #reached final page

    #loop over entries on page 
    #passing className in dict because class is reserved word in Pythong
    #in bs >= 4.1.2 could also use keyword class_
    for entry in soup.find_all(tagName,{'class':className}):
      print entry.get_text()

    #avoid sending too many requests in short space of time
    time.sleep(crawlDelay)
