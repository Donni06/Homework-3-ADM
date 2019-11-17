# Preprocessing libraries
import nltk
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

import pandas as pd
import os.path

from tqdm import tqdm_notebook

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