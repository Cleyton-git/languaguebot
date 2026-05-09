import os
import csv
from itertools import islice
from . import telas, enviar_telegram
from ..models import FraseUsuario, UsuarioOndoku

def pegar_palavra(user):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(BASE_DIR, "database.txt")

    with open(caminho, "r", encoding="utf-8") as r:
        reader = csv.reader(r)
        palavra = list(islice(reader, user.palavra_inicial, user.palavra_inicial + 10))
        print(user.palavra_inicial, palavra)
    return palavra[user.palavra_atual][0], palavra[user.palavra_atual][1], palavra[user.palavra_atual][2]

def processar_palavra(user, req):
    if user.palavra_atual == 10:
        user.palavra_inicial += 10
        user.palavra_atual = 0
        user.tela_atual = "ondoku"
        user.save()
        user_ondoku = UsuarioOndoku.objects.filter(usuario=user.telegram_id).first()
        telas.Tela_ondoku(user, req, user_ondoku)
        return
    palavra = pegar_palavra(user)
    palavra_correta = palavra[0]
    
    if palavra_correta == req:
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg=f"Você apenas digitou {req} digite a palavra em uma frase", func="send_msg")
        return
    elif palavra_correta.lower() not in req.lower().split():
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg=f"Use a palavra '{palavra_correta}' na frase!", func="send_msg")
        return
    
    FraseUsuario.objects.create(
        usuario=user,
        palavra = palavra_correta,
        frase = req
    )
    user.palavra_atual += 1
    user.save()
    
    telas.Tela_frases(user)
    