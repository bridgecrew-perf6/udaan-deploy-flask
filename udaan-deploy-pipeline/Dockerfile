FROM python:3.9


WORKDIR /home/sanskar/NLP-Deployment-Heroku
COPY . .

RUN apt-get update -y
#RUN ./udaan-deploy-pipeline/how-install-tesseract.sh 
RUN apt-get install -y tesseract-ocr libtesseract-dev  poppler-utils tesseract-ocr libtesseract-dev  poppler-utils ffmpeg libsm6 libxext6
RUN apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pillow pytesseract pdf2image pdfreader opencv-python

#RUN gdown <gdrive-url>

CMD python3 main.py
