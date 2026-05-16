import os
import csv
from itertools import islice
from . import telas, enviar_telegram
from ..models import FraseUsuario, UsuarioOndoku
import spacy

nlp = spacy.load("en_core_web_sm")

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
        user.tela_atual = "ask ondoku"
        user.save()
        if user.streak == 0:
            if user.streak == 0:
                enviar_telegram.enviar_telegram(id=user.telegram_id, msg=
                                        "🎧 Você entrou no treino de Ondoku!\n\n"

                                        "Como essa é sua primeira vez aqui, deixa eu te explicar rapidinho.\n\n"

                                        "📈 A cada dia que você estudar, você ganha +1 level_ondoku.\n"
                                        "O level máximo é 30, e a cada nível você desbloqueia novos áudios para treinar.\n\n"

                                        "🔓 Conforme você evolui, novos Ondokus vão sendo liberados.\n"
                                        "Isso significa que você terá conteúdo novo constantemente durante sua jornada.\n\n"

                                        "🔥 Se você chegar até o level 30, serão 30 dias seguidos praticando inglês.\n"
                                        "E sinceramente? Se você fizer isso direito, teu inglês vai melhorar MUITO.", func="send_msg")
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg=f"""🎧 Escolha um Ondoku conforme seu nível:

{"✅ Level 1: Giving personal information" if user.level_ondoku >= 0 else "🔒 Level 1: Giving personal information (Desbloqueia no level 1)"}
{"✅ Level 2: Describing people" if user.level_ondoku >= 5 else "🔒 Level 2: Describing people (Desbloqueia no level 5)"}
{"✅ Level 3: Shopping for clothes" if user.level_ondoku >= 10 else "🔒 Level 3: Shopping for clothes (Desbloqueia no level 10)"}
{"✅ Level 4: Ordering food in a café" if user.level_ondoku >= 15 else "🔒 Level 4: Ordering food in a café (Desbloqueia no level 15)"}
{"✅ Level 5: Tour of London" if user.level_ondoku >= 20 else "🔒 Level 5: Tour of London (Desbloqueia no level 20)"}
{"✅ Level 6: Llamas" if user.level_ondoku >= 25 else "🔒 Level 6: Llamas (Desbloqueia no level 25)"}

📈 Seu nível atual: {user.level_ondoku}
Escolha entre 1 e 6""", func="send_msg")  
        telas.Tela_ask_ondoku(user, req)
        
        return
    palavra = pegar_palavra(user)
    palavra_correta = palavra[0]
    palavra_correta = palavra_correta.lower().strip()
    
    doc = nlp(req)
    lemmas = [token.lemma_.lower().strip() for token in doc]

    if palavra_correta == req.strip().lower(): #apenas a palavra não passa
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg=f"Você apenas digitou {req} digite a palavra em uma frase", func="send_msg")
        return
    if not any(t.lemma_.lower() == palavra_correta or t.text.lower() == palavra_correta for t in doc):
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
    