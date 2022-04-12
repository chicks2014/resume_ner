import os
import pathlib
from pathlib import Path
import sys, fitz
from tika import parser
import textract
# directory = 'resumes'

os.chdir(../resume)
print(os.getcwd())
directory = os.getcwd()

def readtxt(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def read_docx(doc_path):
    pTextString = readtxt(doc_path)
    print (pTextString)
    generatedFile = doc_path + ".txt"
    file = open(generatedFile, "a")
    file.write(str(pTextString)) 
    file.close()

# method-1 : lib: tika
def read_pdf_tika(pdf_path):
    return parser.from_file(pdf_path)['content']

def convert_to_pdf(filename):
    path = pathlib.Path(filename)
    converttopdf(filename)
    file_path_new = os.path.splitext(filename.path)[0]
    file_name_new = Path(file_path_new).stem
    filename1=f' {file_name_new}.pdf'
    filename=pathlib.Path(filename1)

def read_docx_textract():
    pTextString = textract.process(doc_path)

    print(pTextString)

    generatedFile = doc_path + ".txt"

    file = open(generatedFile, "a")
    file.write(str(pTextString)) 
    file.close()

# start scanning resume folder
for filename in os.scandir(directory):
   
    print("--"*50, "\n\n", filename, "--"*50)
    #----------------------------------
    if(filename.path.endswith(".docx")):
        #  read from .docx
        read_docx(filename)
    
    # for pdf
    elif(filename.path.endswith(".pdf")):
        # read from pdf
        result = read_pdf_tika(filename)
        print(result)

    #-------------------------------------------------------
    if(filename.is_file()):
        #print(filename.name)
        frame =filename.path
        with fitz.open(filename.path) as docs:
           tx = ""
           for page in docs:
            tx = tx +str(page.get_text())
            
        text = " ".join(tx.split('\n')) 
        print(text)  
            
    file_path = os.path.splitext(frame)[0]
    file_name = Path(file_path).stem
    #print(file_path)
    #print(file_name)
    out_file=open('sample-resume-textformat/'+file_name,"w",encoding="utf-8")
    out_file.write(text)
    
out_file.close()