import PyPDF2
 
# #create file object variable
# #opening method will be rb
# pdffileobj=open(r'data/3+.pdf','rb')
 
# #create reader variable that will read the pdffileobj
# pdfreader=PyPDF2.PdfFileReader(pdffileobj)
 
# #This will store the number of pages of this pdf file
# x=pdfreader.numPages
# print(x)

# # if pdfreader.isEncrypted:
# #     pdf.decrypt('')

 
# #create a variable that will select the selected number of pages
# pageobj=pdfreader.getPage(1)
 
# #(x+1) because python indentation starts with 0.
# #create text variable which will store all text datafrom pdf file
# text=pageobj.extractText()
 
# #save the extracted data from pdf to a txt file
# #we will use file handling here
# #dont forget to put r before you put the file path
# #go to the file location copy the path by right clicking on the file
# #click properties and copy the location path and paste it here.
# # #put "\\your_txtfilename"
# # file1=open(r"data/3+.txt","a")
# # file1.writelines(text)
# filename = "data/3+.pdf"
# reader = PyPDF2.PdfFileReader(filename,"rb")
# pageObj = reader.getNumPages()
# print(pageobj)
# for page_count in range(pageObj):
#     page = reader.getPage(page_count)
#     page_data = page.extractText()
#     print(page_data)

# import pdftotext
 
# # Load your PDF
# with open("data/3+.pdf", "rb") as f:
#     pdf = pdftotext.PDF(f)
 
# # Save all text to a txt file.
# with open('data/output.txt', 'w') as f:
#     f.write("\n\n".join(pdf))
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

output_string = StringIO()
with open('data/3+.pdf','rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)

# print(output_string.getvalue())
#storing data to text file
text = output_string.getvalue().encode('utf-8')
#writing text data into txt file
with open(r"data/3++.txt","w") as f:
    f.writelines(str(text))

# with open(r"data/3+.txt","r") as f:
#     for line in f:
#         line_out = line.encode('utf-8')
#         print(line_out)
# f = open("data/3+.txt", "rb")
# text1 = f.read().decode(errors='replace') 

# with open(r"data/3_decoded+.txt","w") as f:
#     f.writelines(text1)

# from bs4 import BeautifulSoup

# with open("data/3+.txt") as markup:
#     soup = BeautifulSoup(markup.read())

# with open("data/3_decoded+.txt", "w") as f: 
#     f.write(str(soup.get_text().encode('utf-8')))