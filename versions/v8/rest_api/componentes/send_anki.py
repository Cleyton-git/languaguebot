from ..models import FraseUsuario
import requests
import genanki
import requests
from io import BytesIO
from . import enviar_telegram
from datetime import date

def create_model():
    my_model = genanki.Model(
            1607392319,
            'Model_BotEnglish',
            fields=[
                {'name': 'Front'},
                {'name': 'Back'},
            ],
            templates=[
                {
                'name': 'Card 1',
                'qfmt': '{{Front}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
                },
            ])
    return my_model
    
def create_deck():
    my_deck = genanki.Deck(2059400110, 'English_Vocab')
    return my_deck

def create_apkg(model, deck, id):
    data = date.today()
    frases = FraseUsuario.objects.filter(usuario=id).all()
    for c in frases:
        my_note = genanki.Note(model=model, fields=[c.palavra, c.frase]) 
        deck.add_note(my_note)
    apkg_file = BytesIO()
    genanki.Package(deck).write_to_file(apkg_file)
    apkg_file.seek(0)
    r = requests.post("https://api.telegram.org/bot8249452727:AAExS5DziVnWEUy2kXO-pwFZ5nmhiCt2aBs/sendDocument",
                  files={"document": (f"deck_{data.day}-{data.month}-{data.year}.apkg", apkg_file)}, data={"chat_id": id})
    return r.json()['ok']

def send_anki_auto(user, c):
    user_frase = FraseUsuario.objects.filter(usuario=user.telegram_id)[c]
    nota = {
        "deckName": "Default",
        "modelName": "Basic",
        "fields": {
            "Front": user_frase.palavra,
            "Back": user_frase.frase
            },
        }
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {"note": nota}
    }
    response = requests.post("http://localhost:8765", json=payload)
    print(response.json()['error'])
    if response.json()['error'] == None:
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg=f"A palavra {user_frase.palavra} foi adicionada no anki", func="send_msg")
    else:
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg=f"A palavra {user_frase.palavra} ja esta no anki, ela não foi adicionada", func="send_msg")
    return
