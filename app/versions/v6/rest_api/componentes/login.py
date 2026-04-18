from ..models import Usuario, Id
from .telas import Tela1, Tela_stats
from rest_framework import status
from rest_framework.response import Response


def Login(id, first_req):
    user_exists_check = Usuario.objects.filter(telegram_id=id)
    if user_exists_check:
        if first_req == "0":
            Tela_stats(user_exists_check)
        elif first_req == "1":
            print("Você entrou no modo jornada!")
        return "response_stop"
    if len(first_req) == 11:
        if first_req[0:7] == "/ativar":
            user_check = Usuario.objects.filter(telegram_id=id)
            if user_check:
                print("Você ja usou o seu código de login, tente usar esse em outro dispositivo")
                return 
            ids = Id.objects.all()
            for c in ids:
                if first_req[-3:] == c.id:
                    Usuario.objects.create(
                        telegram_id=id
                    )
                    Id.objects.filter(id=c.id).delete()
                    print("Você usou seu código de ativação do bot, o código expirou")
                    return "logado"
    else:
        print("Você deve digitar /ativar e seu código para ativar o bot")
        