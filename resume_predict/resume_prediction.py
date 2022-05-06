import pandas as pd
import torch
from transformers import BertTokenizer, BertForTokenClassification, BertTokenizerFast
from datetime import datetime


from torch import cuda
device = 'cuda' if cuda.is_available() else 'cpu'
print('Device - ' + device)

import os
import glob


class resume_predicter:

    def __init__(self, pSavedModelPath, pInferenceResumeFileExtractPath, pPredictionSavePath):
        self.pSavedModelPath = pSavedModelPath
        self.pInferenceResumeFileExtractPath = pInferenceResumeFileExtractPath
        self.pPredictionSavePath = pPredictionSavePath

        # import os
        # os.getcwd()
        # from google.colab import drive
        # drive.mount('/content/drive')
        # os.chdir('/home/vn/Documents/iN/iNLP/resume_ner/saved_models/01_model_180422_Vimal')
        # pSavedModelPath = os.getcwd()

    '''
    wordTagAutoAnnotation(sentence):
    Feature: Inference function. Inference the Tags for each word on the Sentence.  
    Input: Sentence with less than 128 charecters.
    Exception: Tags will not be generated for charecters more than 128. 
    '''
    def wordTagAutoAnnotation(self, sentence, ids_to_labels, MAX_LEN, tokenizer, model):
        try:

            inputs = tokenizer(sentence.split(),
                                #  is_pretokenized=True,  # Commented by Vimal
                                is_split_into_words=True,  # Added by Vimal
                                return_offsets_mapping=True, 
                                padding='max_length', 
                                truncation=True, 
                                max_length=MAX_LEN,
                                return_tensors="pt")

            # move to gpu
            ids = inputs["input_ids"].to(device)
            mask = inputs["attention_mask"].to(device)
            # forward pass
            outputs = model(ids, attention_mask=mask)
            logits = outputs[0]

            active_logits = logits.view(-1, model.num_labels) # shape (batch_size * seq_len, num_labels)
            flattened_predictions = torch.argmax(active_logits, axis=1) # shape (batch_size*seq_len,) - predictions at the token level

            tokens = tokenizer.convert_ids_to_tokens(ids.squeeze().tolist())
            token_predictions = [ids_to_labels[i] for i in flattened_predictions.cpu().numpy()]
            wp_preds = list(zip(tokens, token_predictions)) # list of tuples. Each tuple = (wordpiece, prediction)

            prediction = []
            for token_pred, mapping in zip(wp_preds, inputs["offset_mapping"].squeeze().tolist()):                
                #only predictions on first word pieces are important
                if mapping[0] == 0 and mapping[1] != 0:
                    prediction.append(token_pred[1])
                else:
                    continue

            # print(sentence.split())
            # print(prediction)

            pSentenceArray = sentence.split()
            # print(len(pSentenceArray))
            # print(len(prediction))

            dataFrameResult1 = pd.DataFrame(pSentenceArray, columns=['Word'])
            dataFrameResult1['Tag'] = prediction
            # dataFrameResult1.head(50)
            dataFrameResult1

            return dataFrameResult1

        except Exception as e:
            print("ERROR : preprocess", e)


    def resume_text_load(self):

        try:

            now = datetime.now()
            date_time_now = now.strftime("%d-%m-%Y_%H-%M-%S")

            print('date_time_now - ' + date_time_now)

            # pSavedModelPath = '/home/vn/Documents/iN/iNLP/resume_ner/saved_models/01_model_180422_Vimal'
            # pInferenceResumeFileExtractPath = '/home/vn/Documents/iN/iNLP/resume_ner/resumes/prediction/05_resume_pre_processed/Aayushi_Bagga.pdf.txt'

            pInferenceResumeFileExtractPath_list_of_files = glob.glob(self.pInferenceResumeFileExtractPath) # * means all if need specific format then *.csv
            pInferenceResumeFileExtractPath_latest_file = max(pInferenceResumeFileExtractPath_list_of_files, key=os.path.getctime)
            print(pInferenceResumeFileExtractPath_latest_file)

            pInferenceResumeFileExtractPathFileName = (pInferenceResumeFileExtractPath_latest_file.rsplit('/', 1)[-1])[:-4]
            pPredictionSaveFileName = self.pPredictionSavePath + '/' + pInferenceResumeFileExtractPathFileName + '_' + date_time_now +'.csv'

            # Read the preprocessed resume text file 
            with open(pInferenceResumeFileExtractPath_latest_file,'r',encoding = "utf-8") as f:
                                text_data = f.read()
            # print('\n')
            # print(text_data)
            print('Read Resume file - ' + pInferenceResumeFileExtractPath_latest_file)

            # Split the sentences using .nline
            pResumeFileExtractList = text_data.split(' .nline ')
            pResumeFileExtractList[:10]

            # Load the sentences in to the wordTagAutoAnnotation function and get the word tag dataframe as output
            pResult00 = pd.DataFrame()
            pResult01 = pd.DataFrame()

            # provide the ids and corresponding labels used for training the model
            ids_to_labels = {
            0: 'B-NAME',
            1: 'I-NAME',
            2: 'O',
            3: 'B-DESIGNATION',
            4: 'I-DESIGNATION',
            5: 'B-SKILLS',
            6: 'I-SKILLS',
            7: 'B-EDUCATION',
            8: 'B-TOTALEXPERIENCE',
            9: 'I-TOTALEXPERIENCE',
            10: 'B-COMPANY',
            11: 'I-COMPANY',
            12: 'B-PROJECTS',
            13: 'I-PROJECTS',
            14: 'B-EMAIL',
            15: 'B-PHONE',
            16: 'B-CERTIFICATES',
            17: 'I-CERTIFICATES',
            18: 'I-EDUCATION',
            19: 'I-PHONE'
            }

            # len(ids_to_labels)

            # Load the Saved Model from the training
            model = BertForTokenClassification.from_pretrained(self.pSavedModelPath, num_labels=len(ids_to_labels))
            model.to(device)

            # Load the Tokenizer from the Saved Model 
            MAX_LEN = 128
            tokenizer = BertTokenizerFast.from_pretrained(self.pSavedModelPath)

            for sentence in pResumeFileExtractList:
                pResult00 = self.wordTagAutoAnnotation(sentence, ids_to_labels, MAX_LEN, tokenizer, model)
                pResult01 = pd.concat([pResult01, pResult00], axis=0, ignore_index=True)

            # Output Dataframe
            # print('\n')
            # print(pResult01.head(50))
            # print('\n')

            # Save data frame to csv file
            pResult01.to_csv(path_or_buf=pPredictionSaveFileName, sep=',', na_rep='O',columns=None, header=True, index=True, index_label=None, mode='w', encoding=None, compression='infer', quoting=None, quotechar='"', line_terminator=None, chunksize=None, date_format=None, doublequote=True, escapechar=None, decimal='.', errors='strict')
            # pResult01.to_csv(pPredictionSaveFileName, encoding='utf-8', index=False)

            print("Predictions are saved in the File - " + pPredictionSaveFileName)


            """# **Convert Dataframe to JSON**
            Use the one of the relevent output format for the webApp
            """
            '''
            # JSON Output Format 01

            resume_inference_json_ouptput_01 = pResult01.to_json(orient = 'index')

            print(resume_inference_json_ouptput_01)

            # JSON Output Format 02

            resume_inference_json_ouptput_02 = pResult01.to_json(orient = 'table')

            print(resume_inference_json_ouptput_02)

            # JSON Output Format 03

            pResult02 = pResult01
            pResult02 = pResult02.reset_index()
            resume_inference_json_ouptput_03 = pResult02.to_json(orient = 'records')

            print(resume_inference_json_ouptput_03)

            # JSON Output Format 04

            resume_inference_json_ouptput_04 = pResult01.to_json(orient = 'columns')

            print(resume_inference_json_ouptput_04)

            # JSON Output Format 05

            resume_inference_json_ouptput_05 = pResult01.to_json(orient = 'records')

            print(resume_inference_json_ouptput_05)

            '''

            print('\n')
        
        except Exception as e:
            print("ERROR : preprocess", e)
