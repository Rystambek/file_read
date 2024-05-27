import os
import re
import csv
from django.http import HttpResponse
from collections import Counter
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import UploadedFile
from docx import Document

def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_words(text):
    # Matndan so'zlarni ajratib olish, "o'" va "g'" so'zlarini qo'shish
    words = re.findall(r'\b[a-zA-Z\'’\'`\'‘]+\b', text)
    return words

def sort_words_alphabetically_with_counts(words):
    word_counts = Counter(words)
    sorted_word_counts = sorted(word_counts.items(), key=lambda item: item[0].lower())
    return sorted_word_counts

def sort_words_by_last_letter(words):
    word_counts = Counter(words)
    sorted_words = sorted(word_counts.items(), key=lambda word: (word[0][-1].lower(), word[0].lower()))
    return sorted_words

def download_result(request, pk, result_type):
    file_instance = get_object_or_404(UploadedFile, pk=pk)
    file_path = file_instance.file.path
    text = read_docx(file_path)
    text_son = len(text.split())
    words = extract_words(text)
    word_counts = dict(Counter(words))
    word_son = len(word_counts.keys())
    sorted_word_counts = sorted(word_counts.items())
    alifbo = sort_words_alphabetically_with_counts(words)
    alifbo_end = sort_words_by_last_letter(words)

    if result_type == 'sorted_word_counts':
        data = sorted_word_counts
    elif result_type == 'alifbo':
        data = alifbo
    elif result_type == 'alifbo_end':
        data = alifbo_end
    else:
        return HttpResponse(status=404)

    csv_data = '\n'.join([f'{row[0]},{row[1]}' for row in data])

    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'output.csv')

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        file.write(csv_data)

    with open(csv_file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="output.csv"'
        return response

    ctx = {
        'file_instance': file_instance,
        'text': text,
        'word_counts': word_counts.items(),
        "sorted_word_counts": sorted_word_counts,
        "alifbo": alifbo,
        "alifbo_end": alifbo_end,
        "download_link": download_link
    }
    return render(request, 'index.html', ctx)

def file_detail(request, pk):
    file_instance = get_object_or_404(UploadedFile, pk=pk)
    file_path = file_instance.file.path
    text = read_docx(file_path)
    text_son = len(text.split())
    words = extract_words(text)
    word_counts = dict(Counter(words))
    word_son = len(word_counts.keys())
    sorted_word_counts = sorted(word_counts.items())
    alifbo = sort_words_alphabetically_with_counts(words)
    alifbo_end = sort_words_by_last_letter(words)

    selected_data = request.GET.get('selected_data')
    print(selected_data)
    if selected_data == 'sorted_word_counts':
        data_to_download = sorted_word_counts
    elif selected_data == 'alifbo':
        data_to_download = alifbo
    elif selected_data == 'alifbo_end':
        data_to_download = alifbo_end
    else:
        data_to_download = []

    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'output.csv')
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Word', 'Count'])
        for word, count in data_to_download:
            writer.writerow(word, count)
        
    download_link = '/media/output.csv'

    ctx = {
        'file_instance': file_instance,
        'text': text,
        'text_son': text_son,
        'word_son': word_son,
        'word_counts': word_counts.items(),
        "sorted_word_counts": sorted_word_counts,
        "alifbo": alifbo,
        "alifbo_end": alifbo_end,
        "download_link": download_link
    }
    return render(request, 'index.html', ctx)

def upload_file(request):
    files = UploadedFile.objects.all()
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        file_instance = UploadedFile(file=uploaded_file)
        file_instance.save()
        return redirect('upload_file')
    return render(request, 'upload.html', {"files": files})

def delete_file(request, pk):
    file = get_object_or_404(UploadedFile, pk=pk)
    file.delete()
    return redirect('upload_file')
