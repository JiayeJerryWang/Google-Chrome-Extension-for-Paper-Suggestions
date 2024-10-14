# The first task of building the PLSA model is to pre-process the paper documents. We have downloaded all the papers 
# mentioned in the lecture as pdf files. We need to reformat the papers from pdf documents to txt documents, which can 
# be easily read by python. In fact, the difficulty is that many papers have subfields (columns), which are hard to 
# process. The Optical Character Recognition (OCR) method is hard to implement and does not have a good performance 
# for our dataset. We utilized the tree hierarchy of html documents to distinguish different parts of paper documents. 
# In pdf2txt.py, we traverse the folder which contains the paper documents and reformat them from pdf file to html file. 
# Then we extract the content in html file and save as txt file. In that case the paper content can be read by our PLSA 
# model. We already run pdf2txt.py and produced the txt files of papers, so that users do not need to run it again.
import fitz
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
import os
import platform

# For Windows
delimiter = "\\"
dict_path = r'.\papers\pdfs'
html_path = r'.\papers\html'
txt_path = r'.\papers\txts'
# Traverse the folder which contains the paper documents, save the path and name of them
def pdflist(dict_path, html_path):
    file_list = []
    html_name_list = []
    txt_name_list = []
    for files in os.walk(dict_path):
        for file in files[2]:
            if os.path.splitext(file)[1] == '.pdf':
                file_list.append(dict_path + delimiter + file)
                txt_name_list.append(file.replace('.pdf', '.txt'))
                html_name_list.append(html_path + delimiter + file.replace('.pdf', '.html'))
            elif os.path.splitext(file)[1] == '.PDF':
                file_list.append(dict_path + delimiter + file)
                txt_name_list.append(file.replace('.PDF', '.txt'))
                html_name_list.append(html_path + delimiter + file.replace('.PDF', '.html'))
    return file_list, txt_name_list, html_name_list

#reformat paper documents from pdf to html. The method that reformat pdf files from pdf to html, then extract the content and 
#save it as txt is learned from https://www.bilibili.com/read/cv16356882
def pdf2html(input_path, html_path):
    doc = fitz.open(input_path)
    # print(doc)
    html_content = ''
    for page in tqdm(doc):
        html_content += page.get_text('html')
    html_content +="</body></html>"
    with open(html_path, 'w', encoding = 'utf-8', newline='')as fp:
        fp.write(html_content)

#Save paper content as txt based on html
def html2txt(html_path, txt_name):
    hfile = open(html_path, 'r', encoding = 'utf-8')
    htmlhandle = hfile.read()
    soup = BeautifulSoup(htmlhandle, "html.parser")
    for i in soup.find_all('div'):
        for j in i:
            text = str()
            for k in j:
                p = '<span .*?>(.*?)</span>'
                result = re.findall(p,str(k))
                if len(result) == 0:
                    pass
                else:
                    text += result[0]
            # print(text)
            with open(txt_path + delimiter + txt_name,'a',encoding = 'utf-8') as text_file:
                text_file.write(text)
                text_file.write('\n')

def main():
    # Check the current platform to use corresponding styles of paths
    # For Mac OS / Linux
    if platform.system().lower() != "windows":
        global dict_path 
        dict_path = "./papers/pdfs"
        global html_path 
        html_path = "./papers/html"
        global txt_path
        txt_path = "./papers/txts"
        global delimiter 
        delimiter = "/"

    file_list, txt_name_list, html_name_list = pdflist(dict_path, html_path)
    for i in range(len(file_list)):
        pdf2html(file_list[i], html_name_list[i])
        html2txt(html_name_list[i], txt_name_list[i])

if __name__ == '__main__':
    main()