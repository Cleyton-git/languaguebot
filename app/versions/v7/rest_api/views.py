from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .componentes import decisao

@api_view(["POST"])
def chatbot_telegram(request):
    tele_id = request.data['message']['chat']['id'] # pega o id
    req = request.data['message']['text'] # pega a req 
    decisao.dec(tele_id, req) # função que faz TODO o back end fora desse arquivo, TODO O BACK END
    return Response(status=status.HTTP_200_OK)
