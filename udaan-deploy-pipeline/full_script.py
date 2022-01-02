import os
import sys
import git_push



def create_final_set(prj_name, pdf_path, ocr_lang, trans_lang, user_git_id, pdftoimg='false' , ocr_only='true' ,uploader_git_id ='AnujaDumada8'):
        ocr_file = pdf_path
        print('cwd is ', os.getcwd())
        os.chdir('./udaan-deploy-pipeline')
        ocr_script = 'python3 ocr/pdf_to_txt_tesseract_ocr.py ' + ocr_file + ' ' + prj_name +' ' + ocr_lang + ' ' +ocr_only+ ' ' + pdftoimg
        os.system(ocr_script)

        #prj_name = ocr_file.split('/')[-1].replace('.pdf','')
        CWD = '/udaan-deploy-pipeline'
        os.chdir('translate')
        trans_script = 'python3 generate_en_tgt_transfiles_batch_withdicts.py ' + '../output_books/' + prj_name + '/CorrectorOutput  glossaries ' + trans_lang
        print('trans script is ', trans_script)
        if ocr_only == 'false':
                os.system(trans_script)
        else:
                print('OCR_ONLY parameter true...not translating')

        copy_from =  './output_books/' + prj_name 
        os.chdir('../')
        print('end cwd is iline 23', os.getcwd())


        git_push.push_to_git(prj_name, copy_from, user_git_id)
        os.chdir('../..')
        
        print('end cwd is iline 29', os.getcwd())
        os.system ('rm -rf tmp_store/'+prj_name)
        os.system('rm -rf output_books/' + prj_name)
        os.chdir('../')
        print('end cwd is', os.getcwd())
        return True
