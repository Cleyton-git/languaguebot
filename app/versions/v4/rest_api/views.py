from django import http
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import WordSerializer
from .models import Word
from . import funcs

@api_view(["POST"])
def chatbot_telegram(request):
    id = request.data['message']['chat']['id']
    primeira_requisicao = request.data['message']['text']
    lista_opcoes = ["0"]
    flag_1 = False # PAREI AQUI, PRECISO FAZER UM SISTEMA PRÉ O MSG_OR_CALL, A IDEIA DELE É SIMPLESMENTE POSSIBILITAR QUE O USUARIO ENTRE E SAIA DO BOT SEM TER MAIS QUE USAR CALLBACK, QUE É UMA BOSTA
    if primeira_requisicao.lower() == "/start" and flag_1 == False:
        funcs.enviar_telegram(id=id, msg="O BOT FOI INICIADO \n Escolha uma opção \n 0 - Adicionar Palavra", func="send_msg")
        flag = True
        return Response(status=status.HTTP_200_OK)
    elif primeira_requisicao in lista_opcoes and flag_1 == True:
        flag = funcs.msg_or_call(primeira_requisicao)
        if flag:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_200_OK)
    else:
        funcs.enviar_telegram(id=id, msg=f"Digite /start para o bot iniciar", func="send_msg")
        return Response(status=status.HTTP_200_OK)
    
@api_view(["GET"])
def get_all(request):
    if request.method == "GET":
        word = Word.objects.all()
        serializer = WordSerializer(word, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)
