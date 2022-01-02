# How to run 
# python3 pycodes/pdf_to_txt_tesseract_ocr.py test.pdf eng

try:
 from PIL import Image
except ImportError:
 import Image
import cv2
import pytesseract
import os
from pdf2image import convert_from_path
import cv2
import sys
from pdfreader import SimplePDFViewer

def parse_boolean(b):
    return b == "True"



orig_pdf_path = sys.argv[1]
project_folder_name = sys.argv[2]
pdftoimg = sys.argv[5]


outputDirIn='/home/sanskar/NLP-Deployment-Heroku/udaan-deploy-pipeline/output_books/'

outputDirectory=outputDirIn+ project_folder_name
print('output directory is ', outputDirectory)
#create images,text folder
if not os.path.exists(outputDirectory):
  os.mkdir(outputDirectory)

if not os.path.exists(outputDirectory+"/Images"):
  os.mkdir(outputDirectory+"/Images")

imagesFolder=outputDirectory+"/Images"

if not os.path.exists(outputDirectory+"/text_files"):
  os.mkdir(outputDirectory+"/text_files")

imageConvertOption= 'True' 

print("converting pdf to images")
jpegopt={
    "quality": 100,
    "progressive": True,
    "optimize": False
    }

#for simpler filename generation
def simple_counter_generator(prefix="", suffix=""):
    i=0
    while True:
        i+=1
        yield 'p' 

output_file=simple_counter_generator("page",".jpg")
        
if(parse_boolean(imageConvertOption)):
    convert_from_path(orig_pdf_path ,output_folder=imagesFolder, dpi=300,fmt='jpeg',jpegopt=jpegopt,output_file=output_file)

print("images created.")
print(pdftoimg) 
if pdftoimg != 'pdf2img':
  print("Now we will OCR")
  os.environ['IMAGESFOLDER']=imagesFolder
  # os.environ['CWD']='/home/sanskar/udaan-deploy-pipeline'
  os.environ['OUTPUTDIRECTORY']=outputDirectory
  #os.environ['CHOSENFILENAMEWITHNOEXT']=chosenFileNameWithNoExt
  os.system('find $IMAGESFOLDER -maxdepth 1 -type f > $OUTPUTDIRECTORY/tmp.list')

  tessdata_dir_config = r'--tessdata-dir "$/home/sanskar/NLP-Deployment-Heroku/udaan-deploy-pipeline/tesseract-exec/tessdata/"'
  languages=pytesseract.get_languages(config=tessdata_dir_config)
  lcount=0
  tesslanglist={}
  for l in languages:
    if not (l== 'osd'):
      tesslanglist[lcount]=l
      lcount+=1
      print(str(lcount)+'. '+l)



lang = sys.argv[3]
print("Selected language model "+ lang ) #tesslanglist[int(linput)-1])
ocr_only = sys.argv[4]
#print("Default model selected: eng")

os.environ['CHOSENMODEL']= lang #tesslanglist[int(linput)-1]
if not os.path.exists(outputDirectory+"/CorrectorOutput"):
  os.mkdir(outputDirectory+"/CorrectorOutput")
  os.mknod(outputDirectory+"/CorrectorOutput/"+'README.md', mode=0o666)

#Creating Final set folders and files
if not os.path.exists(outputDirectory+"/Comments"):
  os.mkdir(outputDirectory+"/Comments")
  os.mknod(outputDirectory+"/Comments/"+'README.md',mode=0o666)
if not os.path.exists(outputDirectory+"/VerifierOutput"):
  os.mkdir(outputDirectory+"/VerifierOutput")
  os.mknod(outputDirectory+"/VerifierOutput/"+'README.md',mode=0o666)

if not os.path.exists(outputDirectory+"/Inds"):
  os.mkdir(outputDirectory+"/Inds")
  os.mknod(outputDirectory+"/Inds/"+'README.md',mode=0o666)
if not os.path.exists(outputDirectory+"/Dicts"):
  os.mkdir(outputDirectory+"/Dicts")
  os.mknod(outputDirectory+"/Dicts/"+'README.md',mode=0o666)


os.system('cp /home/sanskar/NLP-Deployment-Heroku/udaan-deploy-pipeline/image.xml ' + outputDirectory)
os.system('cp /home/sanskar/NLP-Deployment-Heroku/udaan-deploy-pipeline/project.xml '+ outputDirectory)

if ocr_only == 'false':
  individualOutputDir=outputDirectory+"/CorrectorOutput"
elif ocr_only == 'true':
  individualOutputDir=outputDirectory+"/Inds"


if pdftoimg == 'pdf2img':
    exit(0)
for imfile in os.listdir(imagesFolder):
  print(imagesFolder+"/"+imfile)
  hocr = pytesseract.image_to_pdf_or_hocr(imagesFolder+"/"+imfile, lang=lang, extension='hocr')
  txt = pytesseract.image_to_string(imagesFolder+"/"+imfile, lang=lang)

  with open(individualOutputDir+'/'+imfile[:-3]+'txt', 'w') as f:
    f.write(txt)

  with open(individualOutputDir+'/'+imfile[:-3]+'hocr', 'w+b') as f:
    f.write(hocr)

print('Done')

