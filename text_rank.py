import spacy
import pytextrank

nlp = spacy.load("en_core_web_sm")

nlp.add_pipe("textrank")

with open('./reviews.txt', 'r') as file:
    text = file.read()

doc = nlp(text)

for sent in doc._.textrank.summary(limit_phrases=5, limit_sentences=5):
    print(sent)
