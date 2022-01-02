from flask import Flask,render_template,url_for,request , json
import indicTrans.translator.try_new as tn 
from flask_restful import Api, Resource, reqparse, abort
from flask import send_from_directory
import os 
from werkzeug.utils import secure_filename
import sys
import fitz
sys.path.append('/home/sanskar/NLP-Deployment-Heroku/udaan-deploy-pipeline') 
from full_script import create_final_set


app = Flask(__name__)
api = Api(app)
api_secret_key = ['sanskar@api','ayush@api']
UPLOAD_FOLDER = '/home/sanskar/NLP-Deployment-Heroku/pdf_upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


translation_args = reqparse.RequestParser()
translation_args.add_argument("sentence", type=str, help="Sentence argument is required for translation")



@app.route('/')
def home():
        return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
        en_sents="test"
        if request.method == 'POST':
                message = request.form['message']
                data = str(message)
                en_sents  = tn.translate(data, 'en' , 'hi')
        return render_template('result.html',prediction = en_sents)


@app.route('/upload/<string:key>/<string:github_id>/<string:project_name>/<string:ocr_lang>/<string:trans_lang>/<string:ocr_only>', methods=['POST'])
def upload_file(key , project_name , github_id , ocr_lang , trans_lang , ocr_only):
        ocr_only = ocr_only.lower()
        # print(ocr_only.lower())
        if key not in api_secret_key:
                resp = {'message' : 'Enter valid api key'}
                return resp

        if 'files[]' not in request.files:
                resp = {'message' : 'No file part in the request'}
                return resp

        files = request.files.getlist('files[]')
        if len(files) > 1:
                resp = {'message' : 'Only one file allowed in the request'}
                return resp 

        for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pdf_path = app.config['UPLOAD_FOLDER'] + filename
        status = create_final_set(prj_name = project_name, pdf_path= pdf_path, ocr_lang=ocr_lang, trans_lang=trans_lang, ocr_only=ocr_only ,user_git_id=github_id)

        if status:
                resp = {'message' : 'successfully uploaded' , 'github id' : github_id , 'project name': project_name , 'ocr languange' : ocr_lang , 'translation language' : trans_lang}
        else:
                resp = {'message' : 'Some problem occured !'}
        return resp

@app.route('/translate/<string:src_lang>/<string:trg_lang>' , methods = ['POST'])
def translation(src_lang, trg_lang):
        args = translation_args.parse_args()
        data = args['sentence']
        data = str(data)
        print(data)
        en_sents = tn.translate(data,src_lang,trg_lang)
        print(en_sents)
        return {'translation' : en_sents}

@app.route('/upload/<string:key>/<string:github_id>/<string:project_name>/<string:pdftoimg>', methods=['POST'])
def pdf2img(key , project_name , github_id , pdftoimg):
        pdftoimg = pdftoimg.lower()
        if key not in api_secret_key:
                resp = {'message' : 'Enter valid api key'}
                return resp
        if 'files[]' not in request.files:
                resp = {'message' : 'No file part in the request'}
                return resp

        files = request.files.getlist('files[]')
        if len(files) > 1:
                resp = {'message' : 'Only one file allowed in the request'}
                return resp 

        for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pdf_path = app.config['UPLOAD_FOLDER'] + filename
        if pdftoimg == "pdf2img":
                status = create_final_set(prj_name = project_name, pdf_path = pdf_path, ocr_lang='eng', trans_lang='hi', pdftoimg = pdftoimg ,user_git_id=github_id)
                if status:
                    resp = {'message' : 'successfully uploaded' , 'github id' : github_id , 'project name': project_name}
                else:
                    resp = {'message' : 'Some problem occured !'}
                return resp
        resp = {'message' : 'Some problem occured !'}
        return resp

@app.route('/upload/<string:key>/<string:pages>', methods=['POST'])
def num_of_pages(key , pages):
        pages = pages.lower()
        if key not in api_secret_key:
                resp = {'message' : 'Enter valid api key'}
                return resp
        if 'files[]' not in request.files:
                resp = {'message' : 'No file part in the request'}
                return resp
        if pages != 'pages':
            resp = {'message' : 'Does not exist, check api url'}
            return resp
        files = request.files.getlist('files[]')
        if len(files) > 1:
                resp = {'message' : 'Only one file allowed in the request'}
                return resp 
        for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pdf_path = app.config['UPLOAD_FOLDER'] + filename
        doc = fitz.open(pdf_path) 
        resp = {'number of pages' : doc.page_count}
        os.system('rm -rf ' + pdf_path)
        return resp 

if __name__ == '__main__':
        print('please wait while model loads and server starts up')
        tn.load_model()
        app.run(debug= True , host = "0.0.0.0")

