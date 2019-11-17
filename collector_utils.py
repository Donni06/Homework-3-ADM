#import used
import requests
import urllib
import time

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
