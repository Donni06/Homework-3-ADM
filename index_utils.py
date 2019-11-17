# Preprocessing libraries
import pandas as pd

 #defining a function to save files right away
def save_dict_to_file(dic, file): 
    f = open('{}.txt'.format(file), 'w',encoding="utf8") #open a new file in write mode (empty)
    f.write(str(dic)) #write in it what we need (it will always be a dictionary, hence 'dic')
    f.close() 

documentlist = {} #to keep track of the words in all files. -->  e.g: {doc_i : ['love, 'movie'.....]}

vocabulary = {} #to keep track of all the pre-processed terms and their ids. --> e.g (term_ids) = {'love':3, 'movie':2}

inverted_index = {} #Is the inverted index. term_id as the key and name of the documents as a list of their values. --> e.g: {1: [doc_1, doc_5, ....], 2: [doc_2, doc_4, ....]}

word_index = 0 #this is used to give the id to the words in the vocabulary

def information(data_frame):
    col = []
    for column in df: # is the dataframe called in the index.py -->  df = pd.read_csv(filename, sep='\t', encoding  = 'utf-8')
        
        # take Intro and Plot
        if column == 'Plot' or column == 'Intro':
            if pd.isnull(data_frame[column][0]):     

                try: # enter all the cases in which paragraphs are missing
                    info = str(data_frame[column][1])
                except:
                    # print(filename, "Intro") 
                    return col,('Continue')
            else :
                info = str(data_frame[column][0])
                
            col.append(info.replace('\n',' '))
        
        else:
            # Infobox 
            if pd.isnull(df[column][0]):      

                try:
                    infobox = str(df[column][1])
                except:
                    infobox = ''
            else :
                infobox = str(df[column][0])

            col.append(infobox.replace('\n',' '))

    
    
    return col, ''