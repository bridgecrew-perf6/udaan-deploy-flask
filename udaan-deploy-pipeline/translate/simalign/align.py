import simalign

source_sentence = "Like all insects this cockroach has three pairs of jointed legs and compound eyes."
target_sentence = "सभी कीटों की तरह इस तिलचट्टे की भी तीन जोड़ी संयुक्त टांगें और संयुक्त आँखें होती हैं।"

model = simalign.SentenceAligner()
result = model.get_word_aligns(source_sentence, target_sentence)
print(result)
