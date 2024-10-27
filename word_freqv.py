import spacy
from collections import Counter
import fitz  # PyMuPDF for PDF files
import docx  # python-docx for .docx files
import tkinter as tk
from tkinter import filedialog, messagebox

# Load Spacy model
nlp = spacy.load('en_core_web_sm')

# Functions for summarization
def compute_word_frequencies(text):
    # split text into tokens using spaCy
    doc = nlp(text)
    # take words from tokens, all but stop words (is,the,at...) and punctuation signs (,,?,!,.)
    words = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    # count each occurrance
    word_frequencies = Counter(words)
    # max frequency is equal to max showing word
    max_freq = max(word_frequencies.values(), default=1)
    # for each word in counted ones, count its frequency based on ration with maximum (to 4 decimals at most)
    for word in word_frequencies:
        word_frequencies[word] = round(word_frequencies[word] / max_freq, 4)
    return word_frequencies

def score_sentences(text, word_frequencies):
    # split text into tokens using spaCy
    doc = nlp(text)
    sentence_scores = {}
    # for each sentence count weight of it
    for sentence in doc.sents:
        sentence_score = 0
        word_count = 0
        # for every word in sentence
        for token in sentence:
            word = token.text.lower()
            # check if exists in word frequencies map
            if word in word_frequencies:
                # if does, count as weight
                sentence_score += word_frequencies[word]
                word_count += 1
        # if word count is > 0, count the weight of sentence based on ratio
        if word_count > 0:
            sentence_scores[sentence] = sentence_score / word_count
    return sentence_scores

# sumarize text based on number of sentences
def summarize_text(text, num_sentences=5):
    # calculate word frequencies/weight
    word_frequencies = compute_word_frequencies(text)
    # calculate sentence weight by word weight
    sentence_scores = score_sentences(text, word_frequencies)
    # sort in order
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary = [str(sent) for sent in sorted_sentences[:num_sentences]]
    return summary

# Functions to extract text from different file types
def extract_text_from_pdf(pdf_path):
    text = ""
    # open pdf and extract from each page its text
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

# Extracts text from docx
def extract_text_from_docx(docx_path):
    # open docx and extract text
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Extracts text from txt
def extract_text_from_txt(txt_path):
    # open txt file and load text
    with open(txt_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Determine file type and extract text accordingly
def extract_text(file_path):
    # if file path has extension pdf, extract from pdf
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    # if file path has extension docx, extract from docx
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    # if file path has extension txt, extract from txt
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    # edge case if file is loaded with unsupported file extension
    else:
        messagebox.showerror("Unsupported File Type", "Please select a PDF, DOCX, or TXT file.")
        return None

# GUI setup - file reading
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx"), ("Text files", "*.txt")])
    if file_path:
        text = extract_text(file_path)
        if text:  # Proceed only if text extraction was successful
            try:
                num_sentences = int(sentence_count_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for sentence count.")
                return
            # call of text summarization
            summary = summarize_text(text, num_sentences=num_sentences)
            display_summary(summary)

# Display summary in box
def display_summary(summary):
    summary_text.delete(1.0, tk.END)  # Clear previous text
    summary_text.insert(tk.END, "\n".join(summary))

# Set up main window
root = tk.Tk()
root.title("File Summarizer")
root.geometry("600x450")

# Label and Entry for Sentence Count
sentence_count_label = tk.Label(root, text="Enter number of sentences:")
sentence_count_label.pack(pady=5)

sentence_count_entry = tk.Entry(root, width=5)
sentence_count_entry.insert(0, "5")  # Default value
sentence_count_entry.pack(pady=5)

# Buttons and Text Display
open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack(pady=10)

summary_text = tk.Text(root, wrap=tk.WORD, width=70, height=20)
summary_text.pack(pady=10)

# Run the app
root.mainloop()
