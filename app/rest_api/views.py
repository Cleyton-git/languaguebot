from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .componentes import decisao
from .models import Id
from .componentes import enviar_telegram

@api_view(["POST"])
def chatbot_telegram(request):
    tele_id = request.data['message']['chat']['id'] # pega o id
    req = request.data['message']['text'] # pega a req 
    if req == "/keys":
        show_keys(tele_id)
        return Response(status=status.HTTP_200_OK)
    decisao.dec(tele_id, req)
    return Response(status=status.HTTP_200_OK)

def show_keys(tele_id):
    ids = Id.objects.all()
    list_ids = []
    for c in ids:
        list_ids.append(c.id)
    enviar_telegram.enviar_telegram(id=tele_id, msg=f"Keys disponiveis:\n" + "\n".join(list_ids), func="send_msg")
    return