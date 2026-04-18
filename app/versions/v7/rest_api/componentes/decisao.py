from . import cadastro, telas
from ..models import Usuario, FraseUsuario
from . import enviar_telegram, backend_tela_jornada, send_anki
from django.utils import timezone
from datetime import timedelta

def dec(tele_id, req):
    user = Usuario.objects.filter(telegram_id=tele_id).first()
    if user:
        if user.tela_atual == "logado":
            if req == "/stats":
                telas.Tela_stats(user)
            elif req == "/jornada":
                telas.Tela_jornada(user)
                user.tela_atual = "jornada"
                user.save()
            else:
                telas.Tela_incial(user.telegram_id)
        elif user.tela_atual == "jornada":
            return backend_tela_jornada.processar_palavra(user, req)
        elif user.tela_atual == "anki":
            if req == "/auto":
                for c in range(0, 10):
                    send_anki.send_anki(user, c)
                user.tela_atual = "descanso"
                user.proximo_estudo = timezone.now() + timedelta(hours=24)
                user.save()
                enviar_telegram.enviar_telegram(id=tele_id, msg=f"Você já fez sua jornada hoje. Recomendo descansar e apenas consumir conteúdo em inglês.\nEspere até as {timezone.localtime(user.proximo_estudo).strftime("%H:%M")} de amanhã\n[ /iniciar ] - reinicia o ciclo (não recomendado)", func="send_msg")
            elif req == "/manu":
                model = send_anki.create_model()
                deck = send_anki.create_deck()
                dec = send_anki.create_apkg(model, deck, user)
                if dec:
                    user.tela_atual = "descanso"
                    user.proximo_estudo = timezone.now() + timedelta(hours=24)
                    user.save()
                    enviar_telegram.enviar_telegram(id=tele_id, msg=f"Você já fez sua jornada hoje. Recomendo descansar e apenas consumir conteúdo em inglês.\nEspere até as {timezone.localtime(user.proximo_estudo).strftime("%H:%M")} de amanhã\n[ /iniciar ] - reinicia o ciclo (não recomendado)", func="send_msg")
            FraseUsuario.objects.filter(usuario=tele_id).delete()
            user.streak += 1
            user.save()
        elif user.tela_atual == "descanso":
            if req == "/iniciar":
                telas.Tela_incial(tele_id)
                user.tela_atual = "logado"
                user.proximo_estudo = None
                user.save()
            elif timezone.localtime(user.proximo_estudo).strftime("%H:%M") and timezone.now() >= user.proximo_estudo:
                telas.Tela_incial(tele_id)
                user.tela_atual = "logado"
                user.proximo_estudo = None
                user.save()
            else:
                enviar_telegram.enviar_telegram(id=tele_id, msg=f"Você já fez sua jornada hoje. Recomendo descansar e apenas consumir conteúdo em inglês.\nEspere até as {timezone.localtime(user.proximo_estudo).strftime("%H:%M")} de amanhã\n[ /iniciar ] - reinicia o ciclo (não recomendado)", func="send_msg")
    elif len(req) == 11:
        cadastro.cadastro_user(tele_id, req)
    else: # se não, ele vai retornar o /ativar
        enviar_telegram.enviar_telegram(id=tele_id, msg="Você deve usar /ativar e seu código de ativação \nEX: /ativar 000", func="send_msg")
        