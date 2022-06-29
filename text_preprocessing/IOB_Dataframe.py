import nltk
import pandas as pd
import en_core_web_sm
import numpy as np
import os

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

nlp = en_core_web_sm.load()

source_path = "/content/drive/MyDrive/DL Practice/NLP_PAUL/NLP_Project/testdata"#change the source path accordingly

def tokenize(source_path):
    l1 = [] #define a list
#loop through the directory
    for files in os.listdir(source_path):
  #get the full path of the file which needs to be read
        full_path = os.path.join(source_path,files)

  #open the file that needs to be read
    with open(full_path,encoding = 'utf8') as f:
        text = f.readlines()
        text = "".join(text)
        sent_token = nltk.sent_tokenize(text)#sentence tokenizing using nltk

#loop through the sentence for word tokenizing
        for sentence in sent_token:
            tokenized_text = nltk.word_tokenize(sentence) # word tokenizing using nltk
            l1.append(tokenized_text) #append the tokenized words into a list
    return l1        

tokens = tokenize(source_path)
df = pd.DataFrame({'words':tokens})
df = df.explode('words')

df['sentence'] = df.index

# df.reset_index(drop  = True)
df = df.reset_index()
df = df.drop(columns='index')
df = df[["sentence","words"]]  
df['Tag']='O'    