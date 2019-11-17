#import used
from bs4 import BeautifulSoup

movies1 = BeautifulSoup(open(r"moviespart1.html"), "html.parser") #open all html files with BeautifulSoup from github saved pages

movies1.prettify() #just to see all the html files

urls = [] #create a list with all the urls in github pages
for url in movies1.findAll('a', href=True):
    urls.append(url['href'])
