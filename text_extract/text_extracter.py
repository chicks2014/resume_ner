from distutils.log import error
from typing import Optional
import psutil
from tika import tika as tika_server
from tika import parser
import os
import re
import pdf2image
import pytesseract
from pytesseract import Output, TesseractError
import os
import shutil

# define the resume folder paths
resume_source = "./resumes/01_resume_source"
resume_extracted = "./resumes/02_resume_extracted"
resume_cleaned = "./resumes/04_resume_cleaned"
resume_not_extracted = "./resumes/03_resume_not_extracted"

'''
text_extraction_image_pdf(resume_file_path)
Feature: Extract text data from pdf docuemnts created from image file and save it in a text file.
Input: File path source, file path destination
Exception: Image size up to the limit of 178956970 pixels
'''
def text_extraction_image_pdf(resume_file_path):
    pdf_path = resume_file_path
    pTextString = ""
    if(pdf_path.endswith(".pdf")):
        try:
            print("Attempt to Extract Text from image PDF File : ", pdf_path)
            images = pdf2image.convert_from_path(pdf_path)
            pTotalPages = (len(images))


            for x in range(pTotalPages):
                text = ""    
                pil_im = images[x]
                ocr_dict = pytesseract.image_to_data(pil_im, lang='eng', output_type=Output.DICT)
                # ocr_dict now holds all the OCR info including text and location on the image
                text = " ".join(ocr_dict['text'])
                pTextString = pTextString + "\n" + "\n"+  "\n" + text
                # print(pTextString)
                # return pTextString
        except Exception as e: print(e)                
    return pTextString

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
        existing_tika_process = get_tika_process()    # Changed for Python 3.6
        if (existing_tika_process):
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
            pInvalidPDFFile = False
            pInvalidFile = False
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
                try:
                    pTextStringLength = len(pTextString)
                    print(pTextStringLength)
                    if (pTextStringLength < 1000):
                        print("Note : Total extracted charecters are less than 1000")
                        if(resume_file_path.endswith(".pdf")):
                            pInvalidPDFFile = True
                        else:
                            pInvalidFile = True

                except:
                    print("Note : Extractied Text object is of type NoneType")
                    if(resume_file_path.endswith(".pdf")):
                        pInvalidPDFFile = True
                    else:
                        pInvalidFile = True

                if(pInvalidPDFFile):
                    try:
                        if(resume_file_path.endswith(".pdf")):
                            pTextString = text_extraction_image_pdf(resume_file_path)
                            pTextStringLength = len(pTextString)
                            print("Image PDF Text Extracted : ", pTextStringLength)
                            if (pTextStringLength < 1000):
                                pInvalidFile = True

                    except Exception as e: print(e)

                if(pInvalidFile):
                    try:
                        presume_source_file_path = os.path.join(resume_source, process_file)
                        shutil.copy2(presume_source_file_path, resume_not_extracted)
                        print("Copied the non processed file to the folder")

                    except Exception as e: print(e)
                else:
                    try:
                        # Write the extracted text data in to a file
                        resume_extracted_file_path = os.path.join(resume_extracted, process_file)
                        generatedFile = resume_extracted_file_path + ".txt"

                        file = open(generatedFile, "w")
                        file.write(str(pTextString)) 
                        file.close()                        

                    except Exception as e: print(e)

            except Exception as e: print(e)

    except Exception as e: print(e)

'''
text_cleaning(resume_extracted,resume_cleaned):
Feature: Clean the text on the file. Currently removing the multiple newline and multiple newline with trailing spaces from the text. 
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

                def remove_multiple_new_line(text): 

                    # Replcace multiple new line with trailing spaces with a new line
                    pattern_multiple_new_line_withSpace = r'\n+\s+'
                    p_text_result01 = re.sub(pattern_multiple_new_line_withSpace, '\n', text).strip()

                    # Replcace multiple new line with a new line
                    pattern_multiple_new_line = r'\n+'
                    p_text_result02 = re.sub(pattern_multiple_new_line, '\n', p_text_result01).strip()

                    return p_text_result02

                clean_text = remove_multiple_new_line(text_data)

                pclean_textLength = len(clean_text)
                print(pclean_textLength)

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
# python text_extract/text_extracter.py