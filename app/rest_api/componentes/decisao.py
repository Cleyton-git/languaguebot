from . import cadastro, telas
from ..models import Usuario, FraseUsuario, UsuarioOndoku
from . import enviar_telegram, backend_tela_jornada, send_anki
from datetime import timedelta, date
from django.utils import timezone
import os, tempfile
from deep_translator import GoogleTranslator
import genanki
import requests
from .gerar_zip import criar_zip

def dec(tele_id, req):
    user = Usuario.objects.filter(telegram_id=tele_id).first()
    if user:
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
            user_ondoku = UsuarioOndoku.objects.filter(usuario=user.telegram_id).first()
            telas.Tela_ondoku(user, req, user_ondoku)
            
        elif user.tela_atual == "anki":
            if req.lower() == "/sim":
                frases_user = FraseUsuario.objects.filter(usuario=user.telegram_id).all()
                data = date.today()
                model = send_anki.create_model()
                deck = send_anki.create_deck()
                for c in frases_user:
                    note = genanki.Note(model=model, fields=[c.palavra, c.frase])
                    deck.add_note(note)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".apkg") as tmp:
                    caminho = tmp.name
                genanki.Package(deck).write_to_file(caminho)
                with open(caminho, "rb") as f:
                    apkg_bytes = f.read()
                os.remove(caminho)
                if user.streak == 0:
                    zip_buffer = criar_zip(apkg_bytes, frases_user, incluir_instrucao = True)
                else:
                    zip_buffer = criar_zip(apkg_bytes, frases_user, incluir_instrucao = False)
                requests.post(f"https://api.telegram.org/bot8249452727:AAExS5DziVnWEUy2kXO-pwFZ5nmhiCt2aBs/sendDocument", 
                              data={"chat_id": user.telegram_id}, 
                              files={"document": (f"pacote{data.day}-{data.month}-{data.year}.zip", zip_buffer)})
            FraseUsuario.objects.filter(usuario=user.telegram_id).delete()
            enviar_telegram.enviar_telegram(id=user.telegram_id, msg=f"Você já fez sua jornada hoje. Recomendo descansar e apenas consumir conteúdo em inglês.\nEspere até as {timezone.localtime(user.proximo_estudo).strftime("%H:%M")} de amanhã\n[ /iniciar ] - reinicia o ciclo (não recomendado)", func="send_msg")
            user.tela_atual = "descanso"
            user.proximo_estudo = timezone.now() + timedelta(hours=24)
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
        enviar_telegram.enviar_telegram(id=tele_id, msg="Você deve usar /ativar e seu código de ativação \nEX: /ativar 000", func="send_msg")
        