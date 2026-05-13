from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .componentes import decisao, remind_users, show_keys
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def health(request):
    return HttpResponse("OK", status=200)

@csrf_exempt
def Reminder_users(request):
    remind_users.Func_remind_users()
    return HttpResponse("OK", status=200)

@csrf_exempt
def Reminder_jornada(request):
    remind_users.Func_remind_jornada()
    return HttpResponse("OK", status=200)
    pass

@api_view(["POST"])
def chatbot_telegram(request):
    tele_id = request.data['message']['chat']['id'] # pega o id
    req = request.data['message']['text'] # pega a req 
    
    if req == "/keys":
        show_keys.Func_show_keys(tele_id)
        return Response(status=status.HTTP_200_OK)
    decisao.dec(tele_id, req)
    return Response(status=status.HTTP_200_OK)

