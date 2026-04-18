from . import enviar_telegram
from .backend_tela_jornada import pegar_palavra

def Tela_incial(tele_id):
    enviar_telegram.enviar_telegram(id=tele_id, msg=f"Bem vindo, escolha uma opção\n[ /stats ] - Ver estatisticas\n[ /jornada ] - Iniciar modo jornada", func="send_msg")
    return

def Tela_stats(dados_user):
    tele_id = dados_user.telegram_id
    palavras = dados_user.palavra_inicial
    streak = dados_user.streak
    enviar_telegram.enviar_telegram(id=tele_id, msg=f"{palavras} Palavras ja aprendidas\nVocê ja seguiu a rotina por {streak} dia", func="send_msg")
    
def Tela_jornada(user):
    tele_id = user.telegram_id
    palavra_def = pegar_palavra(user)
    enviar_telegram.enviar_telegram(id=tele_id, msg=f"Digite uma frase com a palavra {palavra_def[0]}", func="send_msg")
    return
