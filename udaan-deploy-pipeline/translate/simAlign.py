import simalign

def map_words(src,tgt):

    sent_src, sent_tgt = src.strip().split(), tgt.strip().split()

    model = simalign.SentenceAligner(model='finetunedL/checkpoint-16000')
    result = model.get_word_aligns(src, tgt)
    #print(source_sentence)
    #print(result['itermax'])

    map={}

    for i,j in result['itermax']:
        map[sent_src[i]]=sent_tgt[j]
    
    return map

src = "Database System Concepts - 7th Edition 17 Silberschatz, Korth and Sudarshan"
tgt = "डाटाबेस सिस्टम कॉन्सेप्ट्स-7वां संस्करण 17 एड्वाइजरी सिलबरचैट्ज़, कोर्थ और सुदर्शन"


op = map_words(src,tgt)
print(op)
f = open("output.txt", "w")
f.write(str(op))
f.close()