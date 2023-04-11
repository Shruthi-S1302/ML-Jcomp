from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from inltk.inltk import tokenize
from inltk.inltk import setup
from indic_transliteration import sanscript
import unicodedata
import urllib.request
import json
from langdetect import detect
import nltk
nltk.download('punkt')

setup('ta')
setup('en')

import os

current_file_dir = os.path.dirname(os.path.abspath(__file__))

stopwords_file_path = os.path.join(current_file_dir, 'TamilStopWords.txt')

# Read Tamil stopwords from file
with open(stopwords_file_path, 'r', encoding='utf-8') as f:
    stopWords = set(f.read().split())

@csrf_exempt
def summarize(request):
    text = request.POST.get('text')
    language = detect(text)
    if language == 'ta':
        words = tokenize(text, "ta")
        filtered_words = [word for word in words if word not in stopWords]
        freqTable = dict()
        for word in filtered_words:
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1
        sentences = text.split('.')
        sentenceValue = dict()
        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence:
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq
        sumValues = 0
        for sentence in sentenceValue:
            sumValues += sentenceValue[sentence]
        average = int(sumValues / len(sentenceValue))
        summary = ''
        for sentence in sentences:
            if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                summary += " " + sentence
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ta&dt=t&q=" + urllib.parse.quote(summary)
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        tamil_summary = data[0][0][0]
        return render(request, 'summary.html', {'summary': tamil_summary})
    else:
        words = nltk.word_tokenize(text)
        filtered_words = [word for word in words if word not in stopWords]
        freqTable = dict()
        for word in filtered_words:
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1
        sentences = nltk.sent_tokenize(text)
        sentenceValue = dict()
        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence:
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq
        sumValues = 0
        for sentence in sentenceValue:
            sumValues += sentenceValue[sentence]
        average = int(sumValues / len(sentenceValue))
        summary = ''
        for sentence in sentences:
            if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                summary += " " + sentence
        print("Summary:" + summary)
        return render(request, 'summary.html', {'summary': summary})
