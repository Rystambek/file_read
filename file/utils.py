# utils.py

import re
from collections import Counter
from docx import Document

def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_words(text):
    # Split the text into words and remove empty strings
    words = re.findall(r'\b[a-zA-Z\']+\b', text)
    return words

def sort_words_alphabetically(words):
    return sorted(words, key=lambda word: word.lower())

def sort_words_by_last_letter(words):
    return sorted(words, key=lambda word: word.lower()[-1])
