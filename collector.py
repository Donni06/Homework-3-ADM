#import used
import requests
import urllib
import time
from bs4 import BeautifulSoup

movies1 = BeautifulSoup(open(r"moviespart1.html"), "html.parser") #open all html files with BeautifulSoup from github saved pages

movies1.prettify() #just to see all the html files

urls = [] #create a list with all the urls in github pages
for url in movies1.findAll('a', href=True):
    urls.append(url['href'])

#create a for loop for download all the url in urls list (collector.py)
c = 0
for url in urls:
    
    try :
        urllib.request.urlretrieve(url, "article{}.html".format(c)) #Copy a network object denoted by a URL to a local file.
        r = requests.get(url)
        time.sleep(2)  #wait 2 seconds each request
        c += 1
        if r.status_code != 200: # (and r.status_code != 404) in case of the page doesn't exist
            raise Exception("Could not download URL" + url)
    except Exception:
        time.sleep(1200) #in the case of the exception happens we stop the program for 20 minutes
