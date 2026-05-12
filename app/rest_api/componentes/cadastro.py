from ..models import Usuario, Id, UsuarioOndoku
from . import enviar_telegram, telas

def cadastro_user(tele_id, req):
    if req[0:7] == "/ativar":
        id_exists = Id.objects.filter(id=req[-3:]).first()
        if id_exists:
            user = Usuario.objects.create(
                nome_usuario = "first_req",
                telegram_id = tele_id,
                palavra_inicial = 0,
                palavra_atual = 0,
                streak = 0,
                tela_atual = "cadastro"
            )
            id_exists.delete()
            pick_name_cadastro(tele_id)
        else:
            enviar_telegram.enviar_telegram(id=tele_id, msg="Código invalido, tente novamente", func="send_msg")
    else:
        enviar_telegram.enviar_telegram(id=tele_id, msg="Você deve digitar /ativar e seu código\nEX: /ativar 000", func="send_msg")
        
def pick_name_cadastro(tele_id):
    enviar_telegram.enviar_telegram(id=tele_id, msg=(
                                                "🎉 Sua key foi ativada com sucesso!\n\n"
                                                "Agora preciso que você escolha um nome para usar no bot.\n\n"
                                                "Pode ser:\n"
                                                "• Seu nome real\n"
                                                "• Um apelido\n"
                                                "• Seu nick de jogos\n"
                                                "• Qualquer nome que você queira ser chamado\n\n"
                                                "✍️ Digite abaixo o nome que deseja usar:"),
                                        func="send_msg")
    
