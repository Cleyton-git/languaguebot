from django.shortcuts import render
from django import http
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import WordSerializer
from .models import Word
import csv
import requests

@api_view(["POST"])
def chatbot_telegram(request):
    try:
        word = request.data['message']['text']
        print(word)
        word = word_trate(word)
        results = get_info_word(word)
        data = {
            "word": word,
            "setences": results[0]
        }
        print(data)
        serializer = WordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

def word_trate(word):
    if word.isalpha():
        word = word.lower().strip()
        return word
    return f"Esse return tem que ser uma msg do chatbot falando que a palavra não é uma palavra"

def get_info_word(word):
    cont = 0
    results = []
    with open("C:/Users/Cleyton/Documents/Github/Python/Projetos/projects/LinguaBot/languaguebot/database/sentences.csv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")

        for row in reader:
            if row[1].upper() == "ENG":
                for c in row[2].split():
                    if c.upper() == word.upper():
                        results.append(row[2])
                        cont += 1
                        if cont == 3:
                            return results

@api_view(["GET"])
def get_all(request):
    if request.method == "GET":
        word = Word.objects.all()
        serializer = WordSerializer(word, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

