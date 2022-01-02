#python3 generate_en_tgt_transfiles_batch_withdicts.py ../output_books/test/output_files/ glossaries hi

from bs4 import BeautifulSoup
import re
from subprocess import check_call
import sys
import os
# importing module (see https://www.geeksforgeeks.org/load-csv-data-into-list-and-dictionary-using-python/)
import csv
import simalign
import string
#from gensim.parsing.preprocessing import strip_punctuation

#Not using the line below
#alignerModel = simalign.SentenceAligner(model='../../Aligners/finetunedL/checkpoint-16000')

# Create your dictionary class (see https://www.geeksforgeeks.org/python-add-new-keys-to-a-dictionary/)
class my_dictionary(dict):
    # __init__ function
    def __init__(self):
        self = dict()
                                  
    # Function to add key:value
    def add(self, key, value):
        self[key] = value
                                                        
# Main Function
dict_obj = my_dictionary()
global_dict={"": ""}
global_mono_dict={"": ""}
                                                          

tgt_lang=sys.argv[3] #languages #'hi'#'ka'#'mr'#'hi'#'te'#'ta'#'or'

#this function is used to merge two bbox boundaries into one
#given x00, y00, x01,y01, x10,y10, x11, y11 through title1 and title2
#return leftmost and topmost x0, y0, and rightmost, bottommost x1, y1
#TODO convert this function to return a polygon shape
def mergebbox(title1, title2):
  
  match1=re.search("^bbox ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)",title1.replace(";",""))
  match2=re.search("^bbox ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)",title2.replace(";",""))

  if(not match1 or not match2):
    print("No bbox? Returning empty title for bbox spec")
    return ''

  bboxret="bbox "
  if(int(match1.group(1))<int(match2.group(1))):
    bboxret+=match1.group(1)+" "
  else:
    bboxret+=match2.group(1)+" "

  if(int(match1.group(2))<int(match2.group(2))):
    bboxret+=match1.group(2)+" "
  else:
    bboxret+=match2.group(2)+" "

  if(int(match1.group(3))>int(match2.group(3))):
    bboxret+=match1.group(3)+" "
  else:
    bboxret+=match2.group(3)+" "

  if(int(match1.group(4).replace(";",""))>int(match2.group(2).replace(";",""))):
    bboxret+=match1.group(4)+";"
  else:
    bboxret+=match2.group(4)+";"
  
  return bboxret

def writeHTranslateFile(baseName):
    hocr_doc=open(baseName+'.hocr','r') #Eg: baseName='HTranslate-Conceptsofphysics1_372_425/Conceptsofphysics1_0001-425'

    htrans_doc_template=open('htranslatetemplate.htranslate','r')

    soup = BeautifulSoup(hocr_doc, 'html.parser')
    newsoup=BeautifulSoup(htrans_doc_template,'html.parser')

    #copy the head tags as is
    newsoup.head=soup.head

    #assuming only one page, copy its name and properties to the new soup
    newpagediv=newsoup.new_tag("div")
    newpagediv['class']=soup.body.div['class']
    newpagediv['id']=soup.body.div['id']
    newpagediv['title']=soup.body.div['title']


    #find all careas
    oldpage=soup.body.div
    careas=oldpage.find_all("div",attrs={"class": "ocr_carea"})
    print("There are "+str(len(careas))+" careas in this hocr document\n")

    for carea in careas:
      paras=carea.find_all("p",attrs={"class": "ocr_par"})
      #print in console when there are more than one paras in a carea as this is unusall and needs
      #to be looked into
      if(len(paras)>1):
        print("There are "+str(len(paras))+" cparas in this hocr document\n")
      for para in paras:
        lines=para.find_all("span",attrs={"class": "ocr_line"})

        if(not lines):
          lines=para.find_all("span",attrs={"class": "ocr_header"})

        if(not lines):
          lines=para.find_all("span",attrs={"class": "ocr_caption"})

        if(not lines):
          lines=para.find_all("span",attrs={"class": "ocr_textfloat"})


        if(not lines):
          print("No lines in header? Unusual! need to check")
          continue

        newpara=newsoup.new_tag("p")
        newpara['class']=para['class']
        newpara['id']=para['id']
        newpara['title']=para['title']
        newpara['lang']=para['lang']

    #a sent can be made of one or more lines, seperated by a word with '.'
        newsentence=None
        isnewsentence=True
        hascompleted=False

        for line in lines:
          words=line.find_all("span",attrs={"class":"ocrx_word"})
          for word in words:
            if not word.string:
              continue
            hascompleted=False
            if(isnewsentence):
              newsentence=newsoup.new_tag("span")
              newsentence.string=""
              newsentence['title']=word['title']
              newsentence['class']="ocr_sent"
              isnewsentence=False
            
            #for now '.' signifies end of sentence
            if('.' in word.string):
              newsentence.string+=word.string
              newsentence['title']=mergebbox(newsentence['title'],word['title'])
              newpara.append(newsentence)
              isnewsentence=True
              hascompleted=True
              continue

            newsentence.string=newsentence.string+word.string+" "
            newsentence['title']=mergebbox(newsentence['title'],word['title'])
        
        if(not hascompleted):
          newpara.append(newsentence)
          
        newpagediv.append(newpara)


    newsoup.body.append(newpagediv)        

    htrans_doc=open(baseName+'.htranslate','w')
    htrans_doc.write(newsoup.prettify())
    htrans_doc.close()
    #print(newsoup.prettify())

    ###############################################

    json_content="{\n\t\"words\": {\n"

    #from bs4 import BeautifulSoup

    #open the .htranslate file
    htrans_doc=open(baseName+'.htranslate','r')

    #get a html soup parser
    soup = BeautifulSoup(htrans_doc, 'html.parser')

    #find all ocr_sent classes
    sentences=newsoup.find_all("span",attrs={"class":"ocr_sent"})

    temptransin_doc=open('temptransin.txt','w')
    local_dict={"": ""}
#    print('sentences are ', sentences)
    for sentence in sentences:
      text2Translate= sentence.string

      #TODO translate change the following line to translation command
      #text2Translate="Translating.. "+text2Translate

      text2Translate = text2Translate.strip('\n')
      temptransin_doc.write(text2Translate+'\n')
      words=text2Translate.split() #See https://www.geeksforgeeks.org/python-string-split/
      for word in words:
          lowercase_word=word.lower()
          if lowercase_word in global_dict.keys():
              local_dict[lowercase_word]=global_dict[lowercase_word]
              #json_content=json_content+"\t\t\""+lowercase_word+"\": [\""+global_dict[lowercase_word]+"\"],\n"




    wordcnt=0
    for key in local_dict: #See https://realpython.com/iterate-through-dictionary-python/
        if(len(key)>0):
            json_content=json_content+"\t\t\""+key+"\": [\""+local_dict[key]+"\"],\n" 
            wordcnt=wordcnt+1

    if(wordcnt>0):
        json_content=json_content[:-1]  #Remove last character (newline)
        json_content=json_content[:-1]  #Remove last character (,)
        json_content=json_content+"\n"  #Add back the newline

    temptransin_doc.close()
    #check_call(["./joint_translate.sh",'temptransin.txt', 'temptransout.txt','en',tgt_lang,'/home/sanskar/NLP-Deployment-Heroku/en-indic'])
    check_call(["./joint_translate.sh",'temptransin.txt', 'temptransout.txt','hi','en','/home/sanskar/NLP-Deployment-Heroku/indic-en'])
    print("Printing translated output")
    temptransout_doc=open('temptransout.txt','r')
    for sentence in sentences:
      text2Translate= sentence.string
      #TODO translate change the following line to translation command
      #text2Translate="Translating.. "+text2Translate

      sentence.string= temptransout_doc.readline()

      #Not using the line below. Seeking alignment based on ../Aligners/simAlign.py
      #alignment = alignerModel.get_word_aligns(text2Translate, sentence.string)

      #sentence.string='A' #text2Translate
      print("Original="+sentence.string)

      text2ReplaceMonoDict = sentence.string.strip('\n')
      #words=sentence.string.split() #See https://www.geeksforgeeks.org/python-string-split/
      words=re.findall(r"[\b\u0900-\u097f\b]+|[.,!?;]", sentence.string,re.UNICODE) #re.findall(r"\b\S+\b|[.,!?;]", dummysentence)
      outputString = ""; 
      changeCount=0;
      for word in words:
          lowercase_word=word.lower()
          if lowercase_word in global_mono_dict.keys():
              word=global_mono_dict[lowercase_word]
              changeCount=changeCount+1
              #json_content=json_content+"\t\t\""+lowercase_word+"\": [\""+global_dict[lowercase_word]+"\"],\n"
          outputString=outputString+" "+word

      if changeCount>0:
          print("Modified="+outputString)

      #Not using the line below. Ideally this should write into another file called cpair
      #print(alignment['itermax'])
      #for key in local_dict: #See https://realpython.com/iterate-through-dictionary-python/
          #if(len(key)>0):
              #cpair[alignment[key]]=local_dict[key] 



    temptransout_doc.close()
    #uncomment following 3 lines to write the translated .htranslate document

    #https://note.nkmk.me/en/python-str-replace-translate-re-sub/
    #baseName=re.sub('\.', '-', baseName)
    htrans_hindi_doc=open(baseName+'.html','w')
    #htrans_hindi_doc=open(baseName+'-'+tgt_lang+'.html','w')
    htrans_hindi_doc.write(newsoup.prettify())
    htrans_hindi_doc.close()
    #print(soup.prettify())


    json_content=json_content+"\t}\n}"
    htrans_dict_doc=open(baseName+'.dict','w')
    htrans_dict_doc.write(json_content)
    htrans_dict_doc.close()

def loadMonoDict(csvfile,domain):
    # opening the file using "with"  statement
    with open(csvfile, 'r') as data:      
        #for line in csv.DictReader(data):
        #for line in csv.reader(data):
        for line in data.read().split("\n"):
            cols = line.split(",")
            if(len(cols)>1):
                cols[1]=re.sub('\"', '', cols[1])
                lowercase_key = cols[0].lower()
                global_mono_dict[lowercase_key] = cols[1].lower() #See https://www.guru99.com/python-dictionary-append.html 

#pure-hindi-list.csv

def loadDict(csvfile,domain):
    # opening the file using "with"  statement
    with open(csvfile, 'r') as data:      
        #for line in csv.DictReader(data):
        #for line in csv.reader(data):
        for line in data.read().split("\n"):
            cols = line.split(",")
            if(len(cols)>1):
                cols[1]=re.sub('\"', '', cols[1])
                lowercase_key = cols[0].lower()
                if lowercase_key in global_dict.keys():
                    global_dict[lowercase_key] = global_dict[lowercase_key]+","+cols[1].lower()+domain #See https://www.guru99.com/python-dictionary-append.html 
                else:
                    global_dict[lowercase_key] = cols[1].lower()+domain #See https://www.guru99.com/python-dictionary-append.html 
                #global_dict[cols[0].lower()] = cols[1].lower()+"("+domain+")" #See https://www.guru99.com/python-dictionary-append.html 
                #dict_obj.add(cols[0],cols[1])

#Agri.csv     Chemistry.csv  ITGlossary.csv    MathKosh.csv  to-include
#biotech.csv  empty          mathGlossary.csv  physics.csv   Zoology.csv

glossarydir = sys.argv[2]
for filename in os.listdir(glossarydir):
    if filename.endswith(".csv"): 
        if "IT" in filename: 
            loadDict(glossarydir+'/'+filename,"(IT)")
        elif "mathGlossary" in filename: 
            loadDict(glossarydir+'/'+filename,"(MA)")
        elif "physics" in filename: 
            loadDict(glossarydir+'/'+filename,"(PH)")
        elif "Zoology" in filename: 
            loadDict(glossarydir+'/'+filename,"(ZO)")
        elif "Chemistry" in filename: 
            loadDict(glossarydir+'/'+filename,"(CH)")
        elif "biotech" in filename: 
            loadDict(glossarydir+'/'+filename,"(BT)")
        elif "Agri" in filename: 
            loadDict(glossarydir+'/'+filename,"(AG)")
        elif "MathKosh" in filename: 
            loadDict(glossarydir+'/'+filename,"(MK)")
        elif "General" in filename: 
            loadDict(glossarydir+'/'+filename,"") #loadDict(glossarydir+'/'+filename,"GE")

loadMonoDict("glossaries/pure-hindi-list.csv","")
print(global_mono_dict)
print("Running test case for monolingual dictionary")

dummysentence="ज़्यादा, गुमराह मत करना क्योंकि अख़बारों"
#dummysentence="Hello, I'm a string!"
print("Original="+dummysentence)
#words=dummysentence.split() #See https://www.geeksforgeeks.org/python-string-split/
#words=re.findall(r"[\w']+|[.,!?;]", dummysentence) #See https://stackoverflow.com/questions/367155/splitting-a-string-into-words-and-punctuation
#words = [item for item in map(string.strip, re.split("(\W+)", dummysentence)) if len(item) > 0] #[t.strip() for t in re.findall(r'\b.*?\S.*?(?:\b|$)', dummysentence, re.UNICODE)]

#From https://stackoverflow.com/questions/367155/splitting-a-string-into-words-and-punctuation
#words=strip_punctuation(dummysentence).split() #re.findall( r'\w+|[^\s\w]+', dummysentence, re.UNICODE)
words=re.findall(r"[\b\u0900-\u097f\b]+|[.,!?;]", dummysentence,re.UNICODE) #re.findall(r"\b\S+\b|[.,!?;]", dummysentence)

print(words)
outputString = ""; 
changeCount=0;
for word in words:
  lowercase_word=word.lower()
  if lowercase_word in global_mono_dict.keys():
      word=global_mono_dict[lowercase_word]
      changeCount=changeCount+1
  outputString=outputString+" "+word

if changeCount>0:
  print("Modified="+outputString)
#quit()

#print(dict_obj)
#print(global_dict)
indir = sys.argv[1]
print('indir is:' , indir)
print('cwd is' , os.getcwd())
for filename in os.listdir(indir):
    print("Considering 2"+filename+" next")
    if filename.endswith(".hocr"): 
        print("Considering 1"+filename+" next")
        # filename=filename.strip('.hocr')
        filename=filename.replace('.hocr','')
        #if filename.startswith("sm_aerospace"): #A fix for some strange problem with hsm aerospace file... It was dropping the h in hsm prefix even though we are stripping the .hocr! So perhaps file names cannot begin with h??!!
            #filename="h"+filename
        print("Accessing "+filename+" next")
        writeHTranslateFile(os.path.join(indir, filename))
        continue
    else:
        continue


