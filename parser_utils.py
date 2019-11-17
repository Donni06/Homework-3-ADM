#import used
from bs4 import BeautifulSoup


# We get the title of the movie
def title (soup): 
    title = soup.select("#firstHeading")[0].text #We used select("#firstHeading") function to take the title
    return title


# In this part we get the INTRO of the movie
def intro(soup):

    try:
        sec = soup.findAll('p')[0] #to get the intro we started parsing  all "p" in wikipedia html page
        if sec == soup.find("p", class_="mw-empty-elt"):
            section_intro = soup.findAll('p')[1] #In this part we go ahead in case the intro has more than one paragraph
      
        else:
            section_intro = sec
        nextNode = section_intro
        intro = [] #create a list to append all intro lines
        intro.append(nextNode.text)

        while True: #create a while loop to make sure you take all the paragraphs and stop when they are over.
            nextNode = nextNode.find_next_sibling()
            if nextNode and nextNode.name == 'p':
                intro.append(nextNode.text)

            else:           
                break         
        intro_s = ""

        for ele in intro: 
            intro_s += ele
            
        return intro_s
    
    except IndexError:
        intro_s = None
        return intro_s

# In this part we get the PLOT of the movie
def plot (soup):
    try:    
      
        sec = soup.findAll('h2')[0] #to get the plot we started parsing all 'h2' in wikipedia html page
        if sec.text == 'Contents' or sec.text == 'Cast': #we skip all not necessary information. 
            section_plot = soup.findAll('h2')[1] #we repeat the same opereation for different 'h2' lines
            if section_plot.text == 'Cast': 
                section_plot = soup.findAll('h2')[1]
        else:
            section_plot = sec
        nextNode = section_plot.find_next_sibling('p')
        plot = []  # create a list to append plot lines

        while True: #create a while loop to make sure you take all the paragraphs and stop when they are over.
            if nextNode and nextNode.name == 'p':
                plot.append(nextNode.text)
                nextNode = nextNode.find_next_sibling()
            else:
                break          
        plot_s = ""

        for ele in plot: 
            plot_s += ele
        return plot_s
    except IndexError:
        plot_s = None 
        return plot_s

# In this part we get the InfoBox of the movie
def infobox(soup):
    try:
        table = soup.find('table', class_='infobox vevent') #We started taking information from the infobox starting from the table in html files
        nextNode = table
        table2 = table.find_all('tr')       
        dic={}  # create a dictionary to store all importart values
        for th in table2[1:]:
            if th.find('th'):            
                dic[th.find('th').text] = th.find('td').get_text(strip=True, separator='|').split('|') #split lines 
         
        standard_dic = {
        "Directed by" : "",
        "Produced by": "",
        "Written by": "",
        "Starring": "",
        "Music by": "", 
        "Release date": "",
        "Running time": "",
        "Country": "",
        "Language": "",
        "Budget": ""} 

        
        shared_items = {k: dic[k] for k in dic.keys() & standard_dic.keys()}  # In this part we check if the keys of the infobox are the same as the ones requested

        for k, v in shared_items.items(): # We transform the list into strings
            shared_items[k] = ", ".join(v)

        value = { k : standard_dic[k] for k in set(standard_dic) - set(dic) }  # Difference, we would like to find the missing INFO of this movie

        value = {k: None if not v else v for k, v in value.items() }  # Replace missing INFO with NaN

        final = dict(shared_items, **value) # Let's combine these two dictionaries

        return final
    
    except AttributeError: #this except is usuful to compare all missing values in the first dictionary Infobox.
        final = {
        "Directed by" : None,
        "Produced by": None,
        "Written by": None,
        "Starring": None,
        "Music by": None, 
        "Release date": None,
        "Running time": None,
        "Country": None,
        "Language": None,
        "Budget": None}   
        
        return final
