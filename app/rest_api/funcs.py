import requests
import csv

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
