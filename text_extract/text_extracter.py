from distutils.log import error
from typing import Optional
import psutil
from tika import tika as tika_server
from tika import parser
import os
import re

# define the resume folder paths
resume_source = "./resumes/resume_source"
resume_extracted = "./resumes/resume_extracted"
resume_cleaned = "./resumes/resume_cleaned"

'''
text_extraction(resume_source,resume_extracted)
Feature: Extract data from pdf, docx, doc and rtf files and save it in a text file.
Input: File path source, file path destination
Exception: pdfs created with images are not extracted
'''
def text_extraction(resume_source,resume_extracted):
    
    try:        

        '''
        tika process is running on a java server. The function will check the status of tika process
        '''
        def get_tika_process() -> Optional[psutil.Process]:
            for process in psutil.process_iter(["name", "cmdline"]):
                if "java" in process.name():
                    for part in process.cmdline():
                        if "tika" in part:
                            return process

        # to stop running process before stating a new one.        
        if existing_tika_process := get_tika_process():
            # print("Found tika process:", existing_tika_process)
            # print("Existing process args:", existing_tika_process.cmdline())
            existing_tika_process.terminate()
            terminate_result = existing_tika_process.wait(10)
            print(f"Terminated tika; exit code {terminate_result}\n")
        else:
            print("No existing tika process found\n")

        tika_server.TikaJavaArgs += "-Xmx1G"

        print("\nStart Resume Extraction")
        print("Source Folder :\n")

        # Loop through the files inside the source folder. Extract text using the tika. 
        for process_file in os.listdir(resume_source):
            file, extension = os.path.splitext(process_file) 
            try:        
                resume_file_path = os.path.join(resume_source, process_file)
                print(resume_file_path)    

                parsed = parser.from_file(resume_file_path)
                # print("Tika server started")
                new_tika_process = get_tika_process()
                if new_tika_process:
                    # print("New process args:", new_tika_process.cmdline())
                    new_tika_process.cmdline()

                # print(parsed["metadata"])        # for getting the file metadata
                pTextString = parsed["content"]  # for getting the file content
                # print(pTextString)
            
                # Write the extracted text data in to a file
                resume_extracted_file_path = os.path.join(resume_extracted, process_file)
                generatedFile = resume_extracted_file_path + ".txt"

                file = open(generatedFile, "a")
                file.write(str(pTextString)) 
                file.close()

            except Exception as e: print(e)

    except Exception as e: print(e)

'''
text_cleaning(resume_extracted,resume_cleaned):
Feature: Clean the text on the file. Currently removing the newline and extra space from the text. 
Input: File path source, file path destination
Exception: Special charecters are currently not removed
'''
def text_cleaning(resume_extracted,resume_cleaned):
    try:
        print("\nStart Resume Cleaning")
        print("Source Folder : \n")
        for process_file in  os.listdir(resume_extracted):
            file, extension = os.path.splitext(process_file) 
            try:
                resume_extracted_file_path = os.path.join(resume_extracted, process_file)
                print(resume_extracted_file_path) 

                resume_cleaned_file_path = os.path.join(resume_cleaned, process_file)
                generatedFile_cleaned = resume_cleaned_file_path

                with open(resume_extracted_file_path,'r',encoding = "utf-8") as f:
                    text_data = f.read()
                    
                # print(text_data)
                    
                def remove_extra_whitespace_tabs(text): 
                    #pattern = r'^\s+$|\s+$' 
                    pattern = r'^\s*|\s\s*' 
                    return re.sub(pattern, ' ', text).strip() 

                clean_text = remove_extra_whitespace_tabs(text_data)

                # print(clean_text)
                    
                with open(generatedFile_cleaned,'w',encoding = "utf-8") as f:
                        f.write(clean_text)

            except Exception as e: print(e)
    except Exception as e: print(e)


# Function Call.
text_extraction(resume_source,resume_extracted)   
text_cleaning(resume_extracted,resume_cleaned)

# use this for running the text_extracter.py file directly
# Create a conda environment inlp01
# conda run -n inlp01 --no-capture-output --live-stream python ./text_extract/text_extracter.py
