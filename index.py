# Preprocessing libraries
import nltk
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

import pandas as pd
import os.path

from tqdm import tqdm_notebook
#Search Engine 1
dir_path = r"C:\Users\loren\Downloads\HW3\TSVFile"
 
# Step 1 concatenates various path components 
for i in tqdm_notebook(range (len(os.listdir(dir_path)))): 
    filename = os.path.join(dir_path, "article_{}.tsv".format(i))
        
    df = pd.read_csv(filename, sep='\t', encoding  = 'utf-8') # Creating a dataframe for each movie
    doc = 'article_{}.tsv'.format(i)
    
    col = []
    col, message = information(df)  
    if message == 'Continue':
        continue
    elif message == 'Pass':
        pass
     
    # Step 2 Taking all the info
       
    to_tokenize = col[0]+col[1]+col[2]+col[3]+col[4]+col[5]+col[6]+col[7]+col[8]+col[9]+col[10]+col[11]+col[12]+col[13]
    tokens = nltk.word_tokenize(to_tokenize) #tokenization
    filtered_words = [nltk.stem.PorterStemmer().stem(word) #removing stopwords, special characters, stemming
                                for word in tokens if word not in nltk.corpus.stopwords.words('english') and word not in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~·']
    
    # Step 3 Creating a document list: for every document we will have the tokenized words 
    documentlist[doc] = filtered_words 
    for w in filtered_words: 
        
        # VOCABULARY
        if w not in vocabulary: 
            word_index += 1    
            vocabulary[w] = word_index  
        
        # INVERTED INDEX
        if vocabulary[w] not in inverted_index: 
            temp = [] 
            temp.append(doc)  
            inverted_index[vocabulary[w]] = temp 
        
        # If the key exists, append the document's name
        elif doc not in inverted_index[vocabulary[w]]: 
            inverted_index[vocabulary[w]].append(doc)  

# Step 4 Save all files
save_dict_to_file(inverted_index,"inverted_index")
save_dict_to_file(vocabulary,"vocabulary")
save_dict_to_file(documentlist,"documentlist")

******************
#Search Engine 2
docpaths = r"C:\Users\loren\Downloads\HW3\TSVFile"
# Step 1 open the previous files.
vocabulary = open('vocabulary.txt', 'r', encoding = 'utf-8')
vocabulary = eval(vocabulary.read()) 

inverted_index = open('inverted_index.txt', 'r', encoding = 'utf-8') 
inverted_index = eval(inverted_index.read())

documentlist = open('documentlist.txt', 'r', encoding = 'utf-8')
documentlist = eval(documentlist.read())

#Step 2 create a new dictionary for the new inverted index
new_inverted_index = {} 
for key,doc in tqdm_notebook(documentlist.items()): #taking the keys (doc_i) and the values 
    
    for w in doc: # w = word in the document
        score = tfidf(w,doc) #tf idf of the word in the doc
        w_index = (key,score) # tuple of key (doc_i), and score (tf/idf)
        if vocabulary[w] not in new_inverted_index: # if the id of the word is not in the new inv_idx
            temp = [] #initializing empty list
            temp.append(w_index) #appending the tuple
            new_inverted_index[vocabulary[w]] = temp #giving to the newly created key (that is the id), the list just created [(doc_i, tf/idf), (doc_i+1, tf/idf)]
        elif doc not in new_inverted_index[vocabulary[w]]: #if the doc is not already in that list: 
            new_inverted_index[vocabulary[w]].append(w_index) #append to the list the new tuple

# Step 3 removing duplicates
for key in new_inverted_index:
    new_inverted_index[key] = list(set(new_inverted_index[key]))
    
# Step 4 saving
save_dict_to_file(new_inverted_index,"inverted_index_tfidf")

