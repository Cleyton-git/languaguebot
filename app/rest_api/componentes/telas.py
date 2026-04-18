from . import enviar_telegram
from .backend_tela_jornada import pegar_palavra
from . import send_anki
from ..models import Usuario, FraseUsuario
from django.utils import timezone
from deep_translator import GoogleTranslator


def Tela_incial(tele_id):
    user = Usuario.objects.filter(telegram_id=tele_id).first()
    palavras_user = user.palavra_atual
    porcentagem = round((palavras_user / 3600) * 100, 1)
    streak = user.streak
    enviar_telegram.enviar_telegram(
    id=tele_id, msg=("👋 Bem-vindo!\n\n"
                     "📊 Seu progresso\n"
                     f"• Palavras aprendidas: {palavras_user} ({porcentagem}%)\n"
                     f"• Streak: {streak} dias 🔥\n\n"
                     "───────────────\n\n"
                     "🚀 O que você quer fazer agora?\n\n"
                     "▶️ /jornada — Iniciar sua sessão de hoje\n"), func="send_msg",)

def Tela_stats(dados_user):
    tele_id = dados_user.telegram_id
    palavras = dados_user.palavra_inicial
    streak = dados_user.streak
    enviar_telegram.enviar_telegram(id=tele_id, msg=f"{palavras} Palavras ja aprendidas\nVocê ja seguiu a rotina por {streak} dia", func="send_msg")
    
def Tela_frases(user):
    tele_id = user.telegram_id
    palavra_def = pegar_palavra(user)
    palavra = palavra_def[0]
    definicao = palavra_def[1]
    frase = palavra_def[2]
    traducao = GoogleTranslator(source='en', target='pt').translate(palavra)
    enviar_telegram.enviar_telegram(
    id=tele_id,
    msg=(
        f"📘 Word: {palavra}\n"
        f"🇧🇷 Tradução: {traducao}\n\n"
        f"💡 Definition:\n{definicao}\n\n"
        f"🧠 Example:\n{frase}\n\n"
        f"✍️ Agora é sua vez:\n"
        f"Escreva uma frase com \"{palavra}\""
    ),
    func="send_msg"
)
    return

def Tela_ondoku(user, req, user_ondoku):
    id = user.telegram_id
    streak = user.streak
    ondoku_atual = user_ondoku.ondoku_atual
    if streak < 10:
        if ondoku_atual == 0:
            enviar_telegram.enviar_telegram(id=user.telegram_id, msg=f"Você esta no treino de fala agora, vc deve:\n1 - Ler o texto em voz alta\n2 - Ouvir o audio do texto\n3 - Ler o texto novamente com o audio", func="send_msg")
            with open("rest_api/componentes/audios/ondoku1.txt", "r") as f:
                texto = f.read()
                linhas = texto.split("\n")
                resultado = []
                
                for linha in linhas:
                    if "Librarian:" in linha:
                        resultado.append("👩 " + linha)
                    elif "Lucy:" in linha:
                        resultado.append("👧 " + linha)
                    else:
                        resultado.append(linha)
                msg="\n".join(resultado)
                
                enviar_telegram.enviar_telegram(id=user.telegram_id, msg=msg, func="send_msg")
            enviar_telegram.enviar_telegram(id=user.telegram_id, msg=f"Digite '/ok' quando terminar", func="send_msg")
            user_ondoku.ondoku_atual += 1
            user_ondoku.save()
        elif req.lower() == "/ok" and ondoku_atual == 1:
            enviar_telegram.enviar_telegram(id=id, func="send_mp3", msg="1")
            enviar_telegram.enviar_telegram(id=id, msg=f"Digite '/ok' quando terminar", func="send_msg")
            user_ondoku.ondoku_atual += 1
            user_ondoku.save()
        elif req.lower() == "/ok" and ondoku_atual == 2:
            enviar_telegram.enviar_telegram(id=id, msg=f"Releia o texto com o audio (se não conseguir apenas releia)", func="send_msg")
            with open("rest_api/componentes/audios/ondoku1.txt", "r") as f:
                texto = f.read()
                linhas = texto.split("\n")
                resultado = []
                
                for linha in linhas:
                    if "Librarian:" in linha:
                        resultado.append("👩 " + linha)
                    elif "Lucy:" in linha:
                        resultado.append("👧 " + linha)
                    else:
                        resultado.append(linha)
                msg="\n".join(resultado)
                
                enviar_telegram.enviar_telegram(id=user.telegram_id, msg=msg, func="send_msg")
            enviar_telegram.enviar_telegram(id=id, msg=f"Digite '/ok' quando terminar", func="send_msg")
            user_ondoku.ondoku_atual += 1
            user_ondoku.save()
        elif req.lower() == "/ok" and ondoku_atual == 3:
            user_ondoku.ondoku_atual = 0
            user_ondoku.save()
            user.tela_atual = "anki"
            user.save()
            enviar_telegram.enviar_telegram(id=user.telegram_id, msg="📘 Seu deck está pronto!", func="send_msg")
            Tela_anki(user, req)
            enviar_telegram.enviar_telegram(id=user.telegram_id, msg="📦 Quer salvar seu progresso? Posso fazer um .zip com palavras, frases e deck de hoje\nDigite /sim se quiser\nDigite qualquer coisa se não", func="send_msg")
        else:
            enviar_telegram.enviar_telegram(id=id, msg=f"Digite /ok", func="send_msg")
    return

def Tela_anki(user, req):
    model = send_anki.create_model()
    deck = send_anki.create_deck()
    dec = send_anki.create_apkg(model, deck, user.telegram_id)
        

def Tela_imersao(user):
    return
    
