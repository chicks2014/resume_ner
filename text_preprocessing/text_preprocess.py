import nltk 
from bs4 import BeautifulSoup
import unicodedata
import re
import string
import spacy
import contractions
import os
from nltk.tokenize import ToktokTokenizer

# function to remove accented characters
def remove_accented_chars(text):
    new_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return new_text  

# function to lemma
def get_lem(text):
    nlp = spacy.load('en_core_web_sm')
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text  
   

def remove_stopwords(text):
    stopword_list = nltk.corpus.stopwords.words('english') 
    tokenizer = ToktokTokenizer()
    # convert sentence into token of words
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    # check in lowercase 
    t = [token for token in tokens if token.lower() not in stopword_list]
    text = ' '.join(t)    
    return text  

# function to expand contractions
def expand_contractions(text):
    return contractions.fix(text)     

# function to remove special characters
def remove_extra_whitespace_tabs(text):
    #pattern = r'^\s+$|\s+$'
    pattern = r'^\s*|\s\s*'
    return re.sub(pattern, ' ', text).strip()  

# function to remove special characters
def to_lowercase(text):
    return text.lower() 


def preprocess(source_path):
    
    with open(source_path,encoding='utf8') as f:
        input_text = f.readlines()
        text = "".join(input_text)
    
    text_lem = get_lem(text)
    text_stopwords = remove_stopwords(text_lem)
    text_contraction = expand_contractions(text_stopwords)
    text_whitespace = remove_extra_whitespace_tabs(text_contraction)
    text_lower = to_lowercase(text_whitespace)

    f.close()

    return text_lower 




def preprocess_text(source_path):
       
    
    for files in os.listdir(source_path):
        full_path = os.path.join(source_path,files)
        preprocess_file = preprocess(full_path)  

        processed_file_path = './resumes'+'/'+"resume_pre_processed"+'/'+ files

        out_file = open(processed_file_path ,"w",encoding="utf-8")
        out_file.write(str(preprocess_file))
        out_file.close() 


    

# os.chdir("d:\\d_drive\\Paul\\NLP\\NLP_resume_parser1\\resume_ner")
source_path = "./resumes/resume_extracted"
preprocess_text(source_path)  
