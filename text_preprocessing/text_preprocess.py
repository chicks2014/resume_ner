
import unicodedata
import re
import os
# import nltk
# import nltk.data 
# import string
# import spacy
# import contractions
# from nltk.tokenize import ToktokTokenizer

# nltk.download('stopwords')
# nltk.download('punkt')

# define the resume folder paths
# resume_cleaned_folder_path = "./resumes/04_resume_cleaned"
# pre_processed_folder_path = "./resumes/05_resume_pre_processed/"

class text_preprocess:

    def __init__(self, resume_cleaned_folder_path, pre_processed_folder_path):
        self.resume_cleaned_folder_path = resume_cleaned_folder_path
        self.pre_processed_folder_path = pre_processed_folder_path

    # function to remove accented characters
    def remove_accented_chars(text):
        new_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        return new_text

    # function to convert to lower case characters
    def to_lowercase(text):
        return text.lower()

        # function to replace new line with .nline

    def replace_newline(text):
        pattern02 = r'\n'
        return re.sub(pattern02, ' .nline ', text).strip()

    # function to remove special characters
    def remove_SpecialCharecters(text):
        pattern = r'[^a-zA-Z0-9 .@\\/:,]'
        return re.sub(pattern, '', text).strip()

        # function to remove white space characters

    def remove_extra_whitespace_tabs(text):
        pattern = r'^\s*|\s\s*'
        test_00 = re.sub(pattern, ' ', text).strip()
        return test_00

    # # function to lemma
    # def get_lem(text):
    #     nlp = spacy.load('en_core_web_sm')
    #     text = nlp(text)
    #     text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    #     return text

    # # function to remove Stop words
    # def remove_stopwords(text):
    #     stopword_list = nltk.corpus.stopwords.words('english')
    #     tokenizer = ToktokTokenizer()
    #     # convert sentence into token of words
    #     tokens = tokenizer.tokenize(text)
    #     tokens = [token.strip() for token in tokens]
    #     # check in lowercase
    #     t = [token for token in tokens if token.lower() not in stopword_list]
    #     text = ' '.join(t)
    #     return text

    # # function to expand contractions
    # def expand_contractions(text):
    #     return contractions.fix(text)

    def preprocess(self, source_path):
        try:
            print(f"\nPre-process started for File: {source_path}")
            with open(source_path, encoding='utf8') as f:
                input_text = f.readlines()
                text = "".join(input_text)

            text_remove_accented_chars = self.remove_accented_chars(text)
            text_to_lower = self.to_lowercase(text_remove_accented_chars)
            text_with_nline = self.replace_newline(text_to_lower)
            text_withOut_specialCharecters = self.remove_SpecialCharecters(text_with_nline)
            text_withOut_whitespace = self.remove_extra_whitespace_tabs(text_withOut_specialCharecters)

            # text_lem = get_lem(text)
            # text_stopwords = remove_stopwords(text_lem)
            # text_contraction = expand_contractions(text_stopwords)

            f.close()

        except Exception as e:
            print("ERROR : preprocess", e)

        return text_withOut_whitespace

    def preprocess_text(self):
        print("\n Start Preprocessing the files.. \n")
        try:
            for files in os.listdir(self.resume_cleaned_folder_path):
                full_path = os.path.join(self.resume_cleaned_folder_path, files)

                preprocess_file = self.preprocess(full_path)

                processed_file_path = self.pre_processed_folder_path + files
                print(f"Destination File-Path:  {processed_file_path}")
                out_file = open(processed_file_path, "w", encoding="utf-8")
                out_file.write(str(preprocess_file))
                out_file.close()
        except Exception as e:
            print("ERROR : preprocess", e)
