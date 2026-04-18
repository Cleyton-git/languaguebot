from ..models import Usuario, Id
from . import enviar_telegram, telas

def cadastro_user(tele_id, req):
    if req[0:7] == "/ativar":
        id_exists = Id.objects.filter(id=req[-3:]).first()
        if id_exists:
            Usuario.objects.create(
                telegram_id=tele_id,
                palavra_inicial = 0,
                palavra_atual = 0,
                streak = 0,
                tela_atual = "logado"
            )
            id_exists.delete()
            enviar_telegram.enviar_telegram(id=tele_id, msg="Você usou seu código de ativação do bot, o código expirou", func="send_msg")
            telas.Tela_incial(tele_id)
        else:
            enviar_telegram.enviar_telegram(id=tele_id, msg="Código invalido, tente novamente", func="send_msg")
    else:
        enviar_telegram.enviar_telegram(id=tele_id, msg="Você deve digitar /ativar e seu código\nEX: /ativar 000", func="send_msg")