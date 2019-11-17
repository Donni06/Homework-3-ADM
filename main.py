import re

import csv
import pandas as pd
from os import listdir
from os.path import isfile, join
import os.path


import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
from nltk.tokenize import sent_tokenize, word_tokenize

import math
import numpy as np
import scipy 
import heapq
from tqdm import tqdm_notebook

# Used for Output
from IPython.display import Markdown, display
def printmd(string):
    display(Markdown(string))


# Functions for second search engine
# Normalized value tf. 'Term frequency' divided by 'document length'. In this way the bias of having a long document doesn't count
def tf(word, document):
    return document.count(word) / len(document) 

# Number of documents with the same word
def document_frequency(word):
    if word in vocabulary:
        term_id = vocabulary[word]
    return len(inverted_index[term_id])

# IDF(word) = log(Total Number Of Documents / Number Of Documents containing the certain term (word))
def idf(word):
    return math.log(len(docpaths) / document_frequency(word))

def tfidf(word, document):
    return tf(word, document) * idf(word)


def importance(dataframe):
    
    if user == 1:
        score_runtime = 0.7
        score_release = 0.3
    elif user == 2:
        score_runtime = 0.3
        score_release = 0.7
    else:
        score_runtime = 0.5
        score_release = 0.5 
    return score_runtime, score_release


# Let's open vocabulary and inverted index in read mode
docpaths = r"C:\Users\Luca\Desktop\-\Università\Magistrale\Primo anno\Primo semestre\ADM\Homeworks\Homework #3"

documentlist = open('documentlist.txt', 'r', encoding = 'utf-8')
documentlist = eval(documentlist.read())

vocabulary = open('vocabulary.txt', 'r', encoding = 'utf-8') 
vocabulary = eval(vocabulary.read()) 

inverted_index = open('inverted_index.txt', 'r', encoding = 'utf-8')  
inverted_index = eval(inverted_index.read())   

inverted_index_tfidf = open('inverted_index_tfidf.txt', 'r', encoding = 'utf-8')  
inverted_index_tfidf = eval(inverted_index_tfidf.read())


# Taking the user's query
query = input() 

# Tokenizing the query
tokens = nltk.word_tokenize(query) 
query_tokens = [nltk.stem.PorterStemmer().stem(token) # Removing stopwords, special characters, stemming
                for token in tokens if token not in stopwords.words('english') if token not in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~·']


search = int(input("Which search engine would you like to pick? \n1. Basic search engine \n2. Search engine with TD*IDF score \n3. Search engine with our own score:\n "))


if search == 1:
    # Taking the term_ids of the query's terms (returns a list of terms_ids) from Vocabulary
    term_ids = [vocabulary[token] for token in query_tokens if token in vocabulary] 

    # Returns the documents in the inverted idx for that have that same ID
    search_results = [inverted_index[i] for i in term_ids if i in inverted_index] 

    # Removing duplicates and preparing for intersection (conjunction)
    new_list = [set(list_) for list_ in search_results]

    # Returns the documents that have all the words of the query
    intersect = set.intersection(*new_list) 
    #Printing the search results
    col_names = ["Title","Intro", 'Url']
    #making a list for the column names
    search1 = pd.DataFrame(columns = col_names) #creating an empty df with the list cerated before
    for j, doc in enumerate(intersect): #iterating through the intersection list and keeping track of the order
        with open(r'TSV\{}'.format(doc), 'r',encoding="utf-8") as file: #opening the files in read mode
            df = pd.read_csv(file, sep='\t', encoding  = 'utf-8')
            df.drop(df.columns.difference(['Title','Intro', 'Url']), 1, inplace=True)

            search1 = pd.concat([df,search1], axis = 0, ignore_index=True, sort = False)

    printmd("The intitial query was: ***{}***".format(query))       
    pd.set_option('max_colwidth',500) #making the rows more readabale(bigger)
    display(search1.style.set_table_styles([ {'selector': '.row_heading, .blank', 'props': [('display', 'none;')]}]))
    
elif search == 2:
    # Score for the query
    tfidf_query_array = [] 
    for w in query_tokens:  
        score = tf(w, query_tokens) * idf(w) 
        tfidf_query_array.append(score) 
    # Terms Id's of the term/s in the query
    term_ids = [vocabulary[token] for token in query_tokens if token in vocabulary] 
    # List of tuples (doc_id, score) for each id
    search_results = [inverted_index_tfidf[idx] for idx in term_ids if idx in inverted_index_tfidf] 

    # Cosine similarity
    cos_arrays = {} 
    for list_ in search_results: 
        for tuple_ in list_: 
            if tuple_[0] not in cos_arrays: 
                temp = []
                temp.append(tuple_[1]) 
                cos_arrays[tuple_[0]] = temp 
            else:
                cos_arrays[tuple_[0]].append(tuple_[1]) 

    # Take the documents that have all of the words
    final = [(key,cos_arrays[key]) for key in cos_arrays if len(cos_arrays[key]) == len(term_ids)] 
    doc_sim = {} #dic for {doc_i : similarity_score, ...}
    for tuple_ in final: #take the tuple in final (the values are the list of the tf/idf scores)
        # Compute the the cosine similarity
        sim = 1 - (scipy.spatial.distance.cosine(np.array(tfidf_query_array) , np.array(tuple_[1]))) 
        # key = doc_id, value = similarity
        doc_sim[tuple_[0]] =  sim 
        
    # OUTPUT    
    # List that has a tuple ordered by the smallest to the largest
    heap = [(-value, key) for key, value in doc_sim.items()] 
    # Taking the largest
    largest = heapq.nsmallest(10, heap) 
    # Ordering keys and values
    largest = [(key, -value) for value, key in largest] 

    #Printing the search results
    col_names = ["Title","Intro", "Similarity", "Url"]
    score_tdidf = pd.DataFrame(columns = col_names) 

    # We use reversed(largest) so that we can add values from the smallest to the greatest
    for j, doc in enumerate(reversed(largest)): 
        with open(r'TSV\{}'.format(doc[0]), 'r',encoding="utf-8") as file: 
            df = pd.read_csv(file, sep='\t', encoding  = 'utf-8')
            df.drop(df.columns.difference(['Title','Intro', 'Url', 'Similarity']), 1, inplace=True)
            df.loc[0, 'Similarity'] = doc[1]
            score_tdidf = pd.concat([df,score_tdidf], axis = 0, ignore_index=True, sort = False)
    
    # Output
    printmd("The intitial query was: ***{}***".format(query))       
    pd.set_option('max_colwidth',500)
    display(score_tdidf.style.background_gradient(cmap='Blues'))

elif search == 3:
    
    # Select the language of the movie you would like to watch
    language = input('What language would you like to see the movie in? ') 

    # Select the runtime and the release year
    user_runtime = int(input('Insert the length of the movie you would like to watch(in minutes): ')) 
    user_release = int(input('Insert the release year of the movie you would like to watch: '))  
    user = int(input("Now, what is more important to you? Is it the running time or the release date?\nAnswer 1 for the first, 2 for the second or 3 for both: "))
    our_score = {}
    # Just to check how many documents have a Null running time or release date
    error = []

    # Iterating through the intersection list created in the 1st search engine
    for j, doc in enumerate(intersect): 
        score = 0 
        df = pd.read_csv(r'TSV\{}'.format(doc), sep='\t', encoding  = 'utf-8')
        if pd.isnull(df['Release date'][0]) == True or pd.isnull(df['Running time'][0]) == True  :
            #print(doc)
            error.append(doc) 
            continue
        else:

            # Checking if the cell of the TSV is already an INT or a STRING
            if type(df['Running time'][0]) != np.int64:
                df['Running time'] = re.sub("[^0-9]", "",df['Running time'][0])

            if type(df['Release date'][0]) != np.int64:
                # Takes the first four numbers of the TSV cell
                s = set(re.findall(r"\b\d{4}\b", df['Release date'][0]))
            if len(s) == 0:
                    continue
                # Taking only the first year of the set
            df['Release date']  = next(iter(s))

            # Is the language we picked the same to the movie we are analyzing?
            if language == df['Language'][0]: 

                score_runtime, score_release = importance(user)


                # If the runtime is included between a range of +- 10 minutes the score increments  
                # or the release date is included between a range of +- 5 years.
                if ((abs(user_runtime) <= abs(int(df['Running time'][0]))+10) and (abs(user_runtime)>= abs(int(df['Running time'][0]))-10)) or ((abs(user_release) <= abs(int(df['Release date'][0]))+5) and (abs(user_release)>= abs(int(df['Release date'][0]))-5)):
                    score = (score_release*1/(abs(int(df['Release date'][0])- user_release)+1)) + (score_runtime*1/(abs(int(df['Running time'][0])- user_runtime)+1))

                # If its outside the range, we apply a penalty = score * 0.5
                else: 
                    score = (score_release*1/(abs(int(df['Release date'][0])- user_release)+1)) + (score_runtime*1/(abs(int(df['Running time'][0])- user_runtime)+1))*0.5
            else:

                continue

        our_score[doc] = score
        
    # OUTPUT
    heap = [(-value, key) for key, value in our_score.items()] 
    largest = heapq.nsmallest(10, heap)
    largest = [(key, -value) for value, key in largest]
    # Printing the search results
    col_names = ["Title","Intro", "Url"]
    our_score = pd.DataFrame(columns = col_names) #creating an empty df with the list cerated before

    # We use reversed(largest) so that we can add values from the smallest to the greatest
    for j, doc in enumerate(reversed(largest)): 
        with open(r'TSV\{}'.format(doc[0]), 'r',encoding="utf-8") as file: #opening the files in read mode
            df_final = pd.read_csv(file, sep='\t', encoding  = 'utf-8')
            df_final.drop(df.columns.difference(['Title','Intro', 'Url']), 1, inplace=True)
            percentage = doc[1]
            df_final['Score'] = percentage
            our_score = pd.concat([df_final,our_score], axis = 0, ignore_index=True, sort = False)

    # Output 
    printmd("The intitial query was: ***{}***".format(query))       
    pd.set_option('max_colwidth',500)
    display(our_score.style.background_gradient(cmap='Blues'))


    

