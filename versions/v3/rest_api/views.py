from django import http
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import WordSerializer
from .models import Word
from . import funcs

@api_view(["POST"])
def chatbot_telegram(request):
    flag = funcs.msg_or_call(request.data)
    if flag:
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_200_OK)
    
@api_view(["GET"])
def get_all(request):
    if request.method == "GET":
        word = Word.objects.all()
        serializer = WordSerializer(word, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)
