from . import cadastro, telas
from ..models import Usuario, FraseUsuario, UsuarioOndoku
from . import enviar_telegram, backend_tela_jornada
from datetime import timedelta, date
from django.utils import timezone
import requests
from .gerar_zip import criar_zip
from . import send_bugs

def dec(tele_id, req):
    user = Usuario.objects.filter(telegram_id=tele_id).first()
    if user:
        if req[:5] == "/help":
            if len(req) == 5:
                print("Digite algo além de só /help")
                return
            send_bugs.Func_send_bugs(tele_id, req[5:])
            return
        
        if user.tela_atual == "logado":
            if req == "/stats":
                telas.Tela_stats(user)
            elif req == "/jornada":
                user.tela_atual = "jornada"
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
            
        elif user.tela_atual == "anki":
            frases_user = FraseUsuario.objects.filter(usuario=user.telegram_id).all()
            frases = []
            for c in frases_user:
                frases.append(c.frase)
            # BLOCO PARA ENVIARA AS FRASES PARA O GPT
            data = date.today()
            
            if user.streak == 0:
                zip_buffer = criar_zip(frases_user, incluir_extras =  True)
            else:
                zip_buffer = criar_zip(frases_user, incluir_extras =  False)
            ### COISAS PARA MUDAR
            #requests.post(f"https://api.telegram.org/bot8249452727:AAExS5DziVnWEUy2kXO-pwFZ5nmhiCt2aBs/sendDocument", 
            #                data={"chat_id": user.telegram_id}, 
            #                files={"document": (f"pacote{data.day}-{data.month}-{data.year}.zip", zip_buffer)})
            requests.post(f"https://api.telegram.org/bot8507566279:AAGN5OQyN8dLhyc3bw8IovGMnfGtgaKpHAA/sendDocument", 
                            data={"chat_id": user.telegram_id}, 
                            files={"document": (f"pacote{data.day}-{data.month}-{data.year}.zip", zip_buffer)})
            
            FraseUsuario.objects.filter(usuario=user.telegram_id).delete()
            enviar_telegram.enviar_telegram(id=user.telegram_id, msg=f"Você já fez sua jornada hoje. Recomendo descansar e apenas consumir conteúdo em inglês por 1h.\nEspere até as {timezone.localtime(user.proximo_estudo).strftime("%H:%M")} de amanhã\n[ /iniciar ] - reinicia o ciclo (não recomendado)", func="send_msg")
            user.tela_atual = "descanso"
            user.proximo_estudo = timezone.now() + timedelta(hours=24)
            user.reminder_user = 1440
            user.streak += 1
            user.save()
            return
            
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
        