#import used
import os.path
import csv
from tqdm import tqdm_notebook #to see the running time

dir_path = r"C:\Users\loren\Downloads\HW3\Movie1" 
 

for i in tqdm_notebook(range (len(os.listdir(dir_path)))): #start a for loop where all the html files are open.
    file_name = os.path.join(dir_path, "article{}.html".format(i))
    with open(file_name, encoding="utf8") as html_file:

        soup = BeautifulSoup(html_file) #Let's start to call the previous functions.
        t = title(soup)
        k = intro(soup)
        p = plot(soup)
        
        canonical_link = soup.find_all("link",{"rel" : "canonical"}) #take the original url for the next search engine. 
        url = canonical_link[0].get('href')

            
        # Write TSV file for each movie, we create a unique dictionary
        dic_title = {'Title' : t}
        dic_intro = {'Intro' : k}
        dic_plot  = {'Plot' : p}
        dic_url = {'Url' : url}
        dic_infobox = infobox(soup)
        
        temp = dict(dic_title, **dic_intro) #create temporary dictionary 
        temp2 = dict(temp, **dic_plot)
        temp3 = dict(temp2, **dic_url)
        final = dict(temp3, **dic_infobox) # it's the unique dictionary we were talking of before
        
        with open(r'TSVFile\article_{}.tsv'.format(i), 'wt', encoding="utf8") as out_file: #save all the tsv file in a new folder.
            tsv_writer = csv.DictWriter(out_file, final.keys(), delimiter ='\t')
            tsv_writer.writeheader()
            tsv_writer.writerow(final)