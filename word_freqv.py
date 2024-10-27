import spacy
from collections import Counter
import re

nlp = spacy.load('en_core_web_sm')

def compute_word_frequencies(text):
    doc = nlp(text)
    words = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    word_frequencies = Counter(words)
    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = round(word_frequencies[word]/max_freq,4)
    return word_frequencies

def score_sentences(text, word_frequencies):
    doc = nlp(text)
    sentence_scores = {}
    for sentence in doc.sents:
        sentence_score = 0
        word_count = 0
        for token in sentence:
            word = token.text.lower()
            if word in word_frequencies:
                sentence_score += word_frequencies[word]
                word_count += 1
        if word_count > 0:
            sentence_scores[sentence] = sentence_score / word_count 
    return sentence_scores
    
def summarize_text(text, num_sentences=5):
    word_frequencies = compute_word_frequencies(text)
    sentence_scores = score_sentences(text, word_frequencies)
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary = [str(sent) for sent in sorted_sentences[:num_sentences]]
    return summary


with open('./reviews.txt', 'r') as file:
    text = file.read()

summary = summarize_text(text, num_sentences=5)

for sentence in summary:
    print(sentence)