import nltk
import nltk.data 
import unicodedata
import re
import string
import spacy
import contractions
import os
from nltk.tokenize import ToktokTokenizer

nltk.download('stopwords')
nltk.download('punkt')

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
   
# function to remove Stop words
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

# function to remove white space characters
def remove_extra_whitespace_tabs(text):
    #pattern = r'^\s+$|\s+$'
    pattern = r'^\s*|\s\s*'
    return re.sub(pattern, ' ', text).strip()  

# function to convert to lower case characters
def to_lowercase(text):
    return text.lower() 

def get_sentences(text):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sn = tokenizer.tokenize(text)
    sn1 = " n_line ".join(sn)
    return sn1

def preprocess(source_path):
    try: 
        print(f"\nPre-process started for File: {source_path}")
        with open(source_path,encoding='utf8') as f:
            input_text = f.readlines()
            text = "".join(input_text)
        
        text_lem = get_lem(text)
        text_stopwords = remove_stopwords(text_lem)
        text_contraction = expand_contractions(text_stopwords)
        text_whitespace = remove_extra_whitespace_tabs(text_contraction)
        text_lower = to_lowercase(text_whitespace)
        text_sent = get_sentences(text_lower)
        f.close()
    except Exception as e:
            print("ERROR : preprocess", e)

    return text_sent 

def preprocess_text(source_path):
    print("\n Start Preprocessing the files.. \n")
    try:
        for files in os.listdir(source_path):    
            full_path = os.path.join(source_path,files)

            preprocess_file = preprocess(full_path)  
            
            processed_file_path = './resumes'+'/'+"05_resume_pre_processed"+'/'+ files
            print(f"Destination File-Path:  {processed_file_path}")
            out_file = open(processed_file_path ,"w",encoding="utf-8")
            out_file.write(str(preprocess_file))
            out_file.close()
    except Exception as e:
            print("ERROR : preprocess", e)

'''
Main function
'''
def main():
    source_path = "./resumes/04_resume_cleaned"
    preprocess_text(source_path)  

# main for function call.
if __name__ == "__main__":
    main()
