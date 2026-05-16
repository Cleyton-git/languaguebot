from . import enviar_telegram
from .backend_tela_jornada import pegar_palavra
from ..models import Usuario, FraseUsuario
from django.utils import timezone
from deep_translator import GoogleTranslator
from ..models import UsuarioOndoku
import threading
from . import integracao_ia

def Tela_incial(tele_id):
    user = Usuario.objects.filter(telegram_id=tele_id).first()
    palavras_user = user.palavra_inicial
    porcentagem = round((palavras_user / 3600) * 100, 1)
    streak = user.streak
    enviar_telegram.enviar_telegram(
    id=tele_id, msg=(f"👋 Bem-vindo! {user.nome_usuario}\n\n"
                     "📊 Seu progresso\n"
                     f"• Palavras aprendidas: {palavras_user} ({porcentagem}%)\n"
                     f"• Streak: {streak} dias 🔥\n\n"
                     "───────────────\n\n"
                     "🚀 O que você quer fazer agora?\n\n"
                     "▶️ /jornada — Iniciar sua sessão de hoje\n"
                     "🛠️ /help para relatar bugs ou melhorias"), func="send_msg",)
    
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

def Tela_ask_ondoku(user, req):
    lista_ops = ["1", "2", "3", "4", "5", "6"]
    print(req)
    if req in lista_ops and user.level_ondoku >= int(req):
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg=
                                        "🎧 Você entrou no treino de fala!\n\n"

                                        "Você deve seguir estes passos:\n\n"#

                                        "1️⃣ Ler o texto em voz alta\n"
                                        "2️⃣ Ouvir o áudio do texto\n"
                                        "3️⃣ Ler o texto novamente junto com o áudio\n\n"

                                        "🔥 Esse treino vai melhorar:\n"
                                        "• Sua pronúncia\n"
                                        "• Sua escuta\n"
                                        "• Sua velocidade no inglês\n"
                                        "• Sua confiança ao falar", func="send_msg")
        user.tela_atual = "ondoku"
        user.save()
        user_ondoku = UsuarioOndoku.objects.get_or_create(usuario=user, defaults={"ondoku_atual": 0, "op_user": int(req)})
        user_ondoku = UsuarioOndoku.objects.filter(usuario=user).first()
        Tela_ondoku(user, req, user_ondoku)
    else:
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg="Digite uma das opções disponiveis", func="send_msg")
        return
    

def Tela_ondoku(user, req, user_ondoku):
    caminho = f"rest_api/componentes/audios/ondoku{user_ondoku.op_user}.txt"
    if user_ondoku.ondoku_atual == 0:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            texto = arquivo.read()
            enviar_telegram.enviar_telegram(id=user.telegram_id, msg=texto, func="send_msg")
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg="Digite /ok quando terminar", func="send_msg")
        user_ondoku.ondoku_atual += 1
        user_ondoku.save()
    elif req == "/ok" and user_ondoku.ondoku_atual == 1:
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg="O telegram esta carregando seu audio...\nPode demorar um pouco", func="send_msg")
        enviar_telegram.enviar_telegram(id=user.telegram_id, func="send_mp3", msg=f"{user_ondoku.op_user}")
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg="Digite /ok quando terminar", func="send_msg")
        user_ondoku.ondoku_atual += 1
        user_ondoku.save()
    elif req == "/ok" and user_ondoku.ondoku_atual == 2:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            texto = arquivo.read()
            enviar_telegram.enviar_telegram(id=user.telegram_id, msg=texto, func="send_msg")
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg="Digite /ok quando terminar", func="send_msg")
        user_ondoku.ondoku_atual += 1
        user_ondoku.save()
    elif req == "/ok" and user_ondoku.ondoku_atual == 3:
        user_ondoku.delete()
        user.tela_atual = "final"
        user.save()
        frases_user = FraseUsuario.objects.filter(usuario=user.telegram_id).all()
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg="🤖 O bot vai analisar suas frases e verificar se elas estão corretas.\n\nIsso pode levar alguns segundos ⏳", func="send_msg")
        threading.Thread(
            target=integracao_ia.Func_integracao_ia,
            args=(user, frases_user),
            daemon=True
        ).start()
    else:
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg="Digite /ok, teste", func="send_msg")
        return
    
def Tela_imersao(user):
    return
    
