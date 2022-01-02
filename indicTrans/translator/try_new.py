from fairseq import checkpoint_utils, distributed_utils, options, tasks, utils
from indicTrans.inference.engine import Model
en2indic_model = None 

def load_model():
	global en2indic_model
	en2indic_model= Model(expdir='en-indic')
	



# # en2indic_model.translate_paragraph(en_paragraph, 'en', 'ta')

# # en2indic_model.batch_translate(en_sents, 'en', 'ta')

# en_paragraph = '''
# 				The pandemic has resulted in worldwide social and economic disruption. 
# 				The world is facing the worst recession since the global financial crisis. This led to the postponement or 
# 				cancellation of sporting, religious, political and cultural events. 
# 				Due to the fear, there was shortage of supply as more people purchased items like masks, sanitizers etc.
# 				'''
def translate(en_p, src_lang, trg_lang):
	en_sents = en2indic_model.translate_paragraph(en_p, src_lang, trg_lang) 
	return en_sents


if __name__ == '__main__':
	en_paragraph = '''
				The pandemic has resulted in worldwide social and economic disruption. 
				The world is facing the worst recession since the global financial crisis. This led to the postponement or 
				cancellation of sporting, religious, political and cultural events. 
				Due to the fear, there was shortage of supply as more people purchased items like masks, sanitizers etc.
				'''
	load_model()
	print(translate(en_paragraph), 'en' , 'hi')
