import json
import os

from os import listdir
from os.path import isfile, join

resume_source = "./train_data_generator/input"
resume_output = "./train_data_generator/output"

'''
read json data from source path
'''
def read_json_data(resume_file_path):
    try:
        f = open(resume_file_path, encoding="mbcs")
        data = json.load(f)
        f.close()
        return data
    except Exception as e:
            print("ERROR : read_json_data : ", e) 

'''
generate as par the spacy format
Example. [('text text text', 'entities':[(start, end, 'NAME'),(start, end, 'EMAIL')])]
'''
def generate_spacy_format(raw_data):
    try:
        # read main text
        text = raw_data[0]['data']['text']
        entities = []
        for i in raw_data[0]['annotations'][0]['result']:
            entities.append([(i['value']['start'],i['value']['end'], i['value']['labels'][0])])

        final_entities = [item[0] for item in entities]
        return [(text, {"entities": final_entities})]
    except Exception as e:
            print("ERROR : generate_spacy_format : ", e) 

'''
Main function
'''
def main():
    for process_file in os.listdir(resume_source):
        print(f"process_file: {process_file}")
        try:        
            resume_file_path = os.path.join(resume_source, process_file)
            print(f"resume_file_path: {resume_file_path}") 

            resume_formatted_file_path = os.path.join(resume_output, process_file)
            print(f"resume_formatted_file_path : {resume_formatted_file_path}")  
            
            raw_data = read_json_data(resume_file_path)
            formatted_data = generate_spacy_format(raw_data)

            # write output file
            with open(resume_formatted_file_path,'w',encoding = "utf-8") as f:
                f.write(str(formatted_data))
        except Exception as e:
            print("ERROR : main", e)

# main for function call.
if __name__ == "__main__":
    main()
