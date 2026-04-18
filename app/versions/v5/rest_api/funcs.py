import requests
import csv
from .models import Word
import genanki
from io import BytesIO
from .serializer import WordSerializer

def word_trate(word, id):
    word = word.lower().strip()
    word = is_word(word, id)
    if word == False:
        return False
    word = is_english(word, id)
    if word == False:
        return False
    return word

def is_word(word, id):
    if word.isalpha() == False:
        enviar_telegram(id, msg=f"A palavra {word} não é compativel, a palavra não deve ter numeros, simbolos ou espaços", func="send_msg")
        return False
    return word

def is_english(word, id):
    with open("C:/Users/Cleyton/Documents/Github/Python/Projetos/projects/LinguaBot/languaguebot/database/sentences_english.txt", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")

        for c in reader:
            for r in c[0].split():
                if r.lower() == word:
                    return word
        enviar_telegram(id, msg=f"A palavra {word} não faz parte do ingles, tente reescrever", func="send_msg")
        return False
    
def enviar_telegram(id, msg_id="", msg="", func=""):
    if func == "send_msg":
        requests.post("https://api.telegram.org/bot8249452727:AAExS5DziVnWEUy2kXO-pwFZ5nmhiCt2aBs/sendMessage", json={
                    "chat_id": id,
                    "text": f"{msg}"
                })
    elif func == "perguntar_import":
        requests.post(f"https://api.telegram.org/bot8249452727:AAExS5DziVnWEUy2kXO-pwFZ5nmhiCt2aBs/sendMessage",
            json={
                "chat_id": id,
                "text": "Como gostaria de enviar suas frases para o Anki?",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {"text": "automatico", "callback_data": "aut"},
                            {"text": "manual", "callback_data": "manu"}
                        ]
                    ]
                }
            }
        )
    elif func == "tirar_auto_manu":
        requests.post(f"https://api.telegram.org/bot8249452727:AAExS5DziVnWEUy2kXO-pwFZ5nmhiCt2aBs/editMessageReplyMarkup",
                json={
                    "chat_id": id,
                    "message_id": msg_id,
                    "reply_markup": {}
                    }
                )
    elif func == "anki_question":
        requests.post(f"https://api.telegram.org/bot8249452727:AAExS5DziVnWEUy2kXO-pwFZ5nmhiCt2aBs/sendMessage",
            json={
                "chat_id": id,
                "text": "Você esta com o anki aberto? ",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {"text": "sim", "callback_data": "sim"},
                            {"text": "não", "callback_data": "não"}
                        ]
                    ]
                }
            }
        )
        
def get_info_word(word):
    results = []
    with open("C:/Users/Cleyton/Documents/Github/Python/Projetos/projects/LinguaBot/languaguebot/database/sentences_english.txt", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")

        for c in reader:
            for r in c[0].split():
                if r == word:
                    results.append(c[0])
                    print(results)
                    return results

def create_model():
    my_model = genanki.Model(
            1607392319,
            'English_BASIC',
            fields=[
                {'name': 'Word'},
                {'name': 'Sentence'},
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
    my_deck = genanki.Deck(2059400110, 'English_VOCAB')
    return my_deck

def create_apkg(model, deck, chat_id):
    word_setences = Word.objects.all()
    for c in word_setences:
        my_note = genanki.Note(model=model, fields=[c.word, c.setences]) 
        deck.add_note(my_note)
    apkg_file = BytesIO()
    genanki.Package(deck).write_to_file(apkg_file)
    apkg_file.seek(0)
    r = requests.post("https://api.telegram.org/bot8249452727:AAExS5DziVnWEUy2kXO-pwFZ5nmhiCt2aBs/sendDocument",
                  files={"document": ("deck.apkg", apkg_file)}, data={"chat_id": chat_id})
    print(r.json())   
    
    
def word_true(data):
    if data.get("callback_query"):
        return False
    elif data.get("message"):
        return True

def if_import(word, id):
    if word == "import":
        enviar_telegram(id, func="perguntar_import")
        return True
    return False

def database_check(word, id):
    everything = Word.objects.filter(pk=word) 
    if everything.exists():
            enviar_telegram(id, f"A palavra {word} ja existe no banco de dados!", "send_msg")
            return True
    return False
        
def send_database(word, results, id):
    serializer = WordSerializer(data={"word": word, "setences": results[0], "anki": False})
    if serializer.is_valid():
        serializer.save()
        enviar_telegram(id, msg=f"A palavra {word} foi adicionada a o banco de dados", func="send_msg")
        return True
    else:
        return False 

def change_database(word):
    Word.objects.filter(word=word).update(anki=True)
    
    
def send_anki(words):
    nota = {
        "deckName": "Default",
        "modelName": "Basic",
        "fields": {
            "Front": words.word,
            "Back": words.setences
            },
        }
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {"note": nota}
    }
    response = requests.post("http://localhost:8765", json=payload)
    return response


def msg_or_call(data):
    print("ENTREI TA")
    return True
    flag = word_true(data)
    if flag == True:
        id = data['message']['chat']['id']
        word = data['message']['text']
        number = data['message']['text']
        word = word_trate(word, id)
        if word == False:
            return False
        check_import = if_import(word, id)
        if check_import == False:
            data_check =  database_check(word, id)
            if data_check == False:
                results = get_info_word(word)
                send_database(word, results, id)
                return False
        return True
    else:
        chat_id = data['callback_query']['message']['chat']['id']
        message_id = data['callback_query']['message']['message_id']
        enviar_telegram(chat_id, message_id, func="tirar_auto_manu")
        if data['callback_query']['data'] == "manu":
            modelo = create_model()
            deck = create_deck()
            create_apkg(modelo, deck, chat_id)
            return True
        else:
            enviar_telegram(id=chat_id, msg="Para enviar de forma automatica vc precisa do ANKI aberto com a extensão ''AnkiConnect'' instalada", func="send_msg")
            word_setences = Word.objects.filter(anki=False)
            tamanho_setences = len(word_setences)
            if tamanho_setences == 0:
                enviar_telegram(id=chat_id, msg=f"Não tem nenhuma palavra nova no banco de dados, adicione alguma!", func="send_msg")
                return True
            for c in word_setences:
                try:
                    response = send_anki(c)
                    if response.json()['error'] == "cannot create note because it is a duplicate":
                        enviar_telegram(id=chat_id, msg=f"A palavra {c.word} ja esta no anki, ela não foi adicionada", func="send_msg")
                    else:
                        enviar_telegram(id=chat_id, msg=f"A palavra {c.word} foi adicionada no anki", func="send_msg")
                        change_database(c.word)
                except requests.exceptions.ConnectionError:
                    enviar_telegram(id=chat_id, msg=f"O anki não esta aberto ou vc não tem a extensão. \n Como instalar: Ferramentas > Extensões > Obter extensões > 2055492159 ", func="send_msg")
                    return True
            return True
