from . import cadastro, telas
from ..models import Usuario, FraseUsuario, UsuarioOndoku
from . import enviar_telegram, backend_tela_jornada, integracao_ia
from datetime import timedelta
from django.utils import timezone
from .gerar_zip import criar_zip
from . import send_bugs
import threading
import os
import json

def dec(tele_id, req):
    user = Usuario.objects.filter(telegram_id=tele_id).first()
    if user:
        if req[:5] == "/help":
            if len(req) == 5:
                enviar_telegram.enviar_telegram(id=tele_id, msg="Digite algo além de só '/help'", func="send_msg")
                return
            threading.Thread(
                target=send_bugs.Func_send_bugs,
                args=(tele_id, req[5:]),
                daemon=True
            ).start()
            enviar_telegram.enviar_telegram(id=tele_id, msg=(
                                                    "✅ Solicitação enviada com sucesso!\n\n"
                                                    "Obrigado por ajudar a melhorar o bot. 💙\n"
                                                    "Sua sugestão/bug foi reportado para análise.\n\n"
                                                    "✍️ Digite qualquer coisa para voltar ao menu normal."
                                                    ), func="send_msg")
            #send_bugs.Func_send_bugs(tele_id, req[5:])
            return
        
        if user.tela_atual == "cadastro":
            enviar_telegram.enviar_telegram(id=tele_id, msg=("👋 Bem-vindo ao bot!\n\n"
                                            "Aqui você segue um ciclo completo para aprender inglês todos os dias:\n\n"
                                            "📚 1. Vocabulário + Escrita\n"
                                            "Você recebe palavras novas e cria suas próprias frases com elas.\n\n"
                                            "🧠 2. Fixação ativa\n"
                                            "Nada de só ler — você pratica escrevendo e usando o inglês de verdade.\n\n"
                                            "🎧 3. Ondoku (Shadowing)\n"
                                            "Você treina com áudio em 3 etapas para destravar sua fala:\n"
                                            "• Lê sozinho\n"
                                            "• Lê junto com o áudio\n"
                                            "• Lê novamente sem ajuda\n\n"
                                            "📦 4. Revisão inteligente\n"
                                            "No final, você recebe seu material do dia para revisar no Anki.\n\n"
                                            "🌍 5. Imersão\n"
                                            "Depois disso, o bot recomenda 1h de conteúdo em inglês para consolidar tudo.\n\n"
                                            "⏱️ Tudo isso em menos de 10 minutos.\n\n"
                                            "🚀 Digite /jornada para começar\n"
                                            "🛠️ /help para relatar bugs ou melhorias"), func="send_msg")
            user.tela_atual = "logado"
            user.nome_usuario = req 
            user.save()
        
        elif user.tela_atual == "logado":
            if req == "/jornada":
                user.tela_atual = "jornada"
                user.reminder_jornada = 0
                user.save()
                telas.Tela_frases(user)
            else:
                telas.Tela_incial(user.telegram_id)
                
        elif user.tela_atual == "jornada":
            return backend_tela_jornada.processar_palavra(user, req)
        
        elif user.tela_atual == "ondoku":
            user_ondoku, created = UsuarioOndoku.objects.get_or_create(
                usuario=user,
                defaults={"ondoku_atual": 0}
            )
            telas.Tela_ondoku(user, req, user_ondoku)
            
        elif user.tela_atual == "final":
            frases_user = FraseUsuario.objects.filter(usuario=tele_id).all()
            
            enviar_telegram.enviar_telegram(id=tele_id, msg="🤖 O bot vai analisar suas frases e verificar se elas estão corretas.\n\nIsso pode levar alguns segundos ⏳", func="send_msg")
            threading.Thread(
                target=integracao_ia.Func_integracao_ia,
                args=(user, frases_user),
                daemon=True
            ).start()
            
        elif user.tela_atual == "descanso":
            if req == "/iniciar":
                telas.Tela_incial(user.telegram_id)
                user.tela_atual = "logado"
                user.proximo_estudo = None
                user.save()
            elif timezone.localtime(user.proximo_estudo).strftime("%H:%M") and timezone.now() >= user.proximo_estudo:
                telas.Tela_incial(user.telegram_id)
                user.tela_atual = "logado"
                user.proximo_estudo = None
                user.save()
            else:
                enviar_telegram.enviar_telegram(id=user.telegram_id, msg=f"Você já fez sua jornada hoje. Recomendo descansar e apenas consumir conteúdo em inglês.\nEspere até as {timezone.localtime(user.proximo_estudo).strftime("%H:%M")} de amanhã\n[ /iniciar ] - reinicia o ciclo (não recomendado)", func="send_msg")
    
    elif len(req) == 11:
        cadastro.cadastro_user(tele_id, req)
        user = Usuario.objects.filter(telegram_id=tele_id).first()
        UsuarioOndoku.objects.create(
                usuario = user,
                ondoku_atual = 0   
            )
    else:
        enviar_telegram.enviar_telegram(id=tele_id, msg="Você deve digitar /ativar e seu código\nEX: /ativar 000\nUse /keys para ver os códigos disponiveis", func="send_msg")
        