from ..models import Usuario, Id

def Login(id, first_req):
    user_exists_check = Usuario.objects.filter(telegram_id=id)
    if user_exists_check:
        return True
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
                    return 
    else:
        print("Você deve digitar /ativar e seu código para ativar o bot")
        