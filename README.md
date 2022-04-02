# udaan-deploy-flask

## How to Run 

1. python3 full-script.py ../../sanskar/book-ocr/license.pdf eng hi

* argument1 -> path of the PDf file
* argument2 -> OCR Language (Currently as eng, hin, urd,san)
* argument3 -> Target translation language (as,bn,gu,hi,kn,ml,mr,or,pa,ta,te)


#### Install individual parts
1. Install indicTrans from https://github.com/AI4Bharat/indicTrans/
2. run how-install-tesseract.sh to install OCR essentials

## Run docker image
1. docker run -p 5000:5000 <img_name>

## Deploy on Cloud run
1. gcloud auth login
2. gcloud auth configure-docker
3. docker tag model_deploy gcr.io/project-id/tag
4. docker push gcr.io/project-id/tag
5. gcloud run deploy --image=gcr.io/<gcloud_project_name>/<each_run_tag_name> --platform=managed --allow-unauthenticated --region=asia-south1 --concurrency=1 --memory=16Gi
