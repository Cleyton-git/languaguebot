from deep_translator import GoogleTranslator
import zipfile
import os
from . import enviar_telegram
import tempfile
from django.utils import timezone

def criar_zip(user, frases, incluir_extras):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
        zip_path = temp_zip.name

    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_STORED) as zipf:
        palavras_txt = gerar_txt_frases(frases)

        zipf.writestr("frases.txt", palavras_txt)

        if incluir_extras:
            bat_content, bat_content_dependencias = gerar_bat()
            py_content = gerar_py()
            lapis_apkg = os.path.join(os.path.dirname(__file__), "Lapis.apkg")

            zipf.writestr("leia-me.txt", gerar_instrucao())            
            zipf.writestr("enviar_anki.bat", bat_content)
            zipf.writestr("instalar_dependencias.bat", bat_content_dependencias)
            zipf.writestr("add_card.py", py_content)

            zipf.write(lapis_apkg, arcname="Lapis.apkg")

    with open(zip_path, "rb") as file:
        enviar_telegram.enviar_telegram(id=user.telegram_id, func="send_zip", file=file)
    os.remove(zip_path)
    
    enviar_telegram.enviar_telegram(id=user.telegram_id, msg=f"Você já fez sua jornada hoje. Recomendo descansar e apenas consumir conteúdo em inglês por 1h.\nEspere até as {timezone.localtime(user.proximo_estudo).strftime("%H:%M")} de amanhã\n[ /iniciar ] - reinicia o ciclo (não recomendado)", func="send_msg")
    

def gerar_txt_frases(frases_user):
    print("CRIANDO TXT")
    conteudo = ""

    for f in frases_user:
        print("ENTROU")
        print(f.palavra)
        print(f.frase)
        traducao = GoogleTranslator(source='en', target='pt').translate(f.palavra)
        conteudo += f"{f.palavra} - {traducao} | {f.frase}\n"
        print("Escreveu")
    
    print("RETORNOU")

    return conteudo

def gerar_instrucao():
    texto = (
        "Como usar o sistema:\n\n"
        "Desktop:\n"
        "1. Clique no instalar_dependencias\n"
        "2. Abra o Lapis.apkg, double click e importe o deck\n"
        "3. Instale o anki connect (ctrl+shift+a/obter extensões, coloque esse código -> 2055492159 e reinicie o anki)\n"
        "4. Apartir daqui você ja pode excluir o instalar_dependencias.bat e o Lapis.apkg\n"
        "5. Clique no enviar_anki (tenha certeza que o anki esta aberto sempre que usar esse .bat)\n"
        "6. Crie uma pasta chamada (data atual ou a maneira que você quiser) e coloque o frases.txt\n"
        "7. REPITA O PROCESSO DO 5 E 6 TODOS OS DIAS\n"
        "8. OBS: NUNCA apague o add_card e o enviar_anki\n"
        "9. Se quiser, pode abaixar o leia-me.txt tbm\n"
        "\nPasso a passo para os proximos dias:\n"
        "1.Faça as tarefas no telegram\n"
        "2.Extraia os arquivos nessa pasta\n"
        "3.Clique no enviar_anki\n"
        "4.Crie a nova pasta com o nome de (data atual) e coloque o frases.txt\n"
        "5.E repete no proximo dia.\n"
        "6.(com o tempo isso vai ser tudo automatizado tbm)\n"
        "Qualquer dúvida ou bug ou recomendação me chamar no email: cleytoncontato281@gmail.com\n"
        "\nAndroid:\n"
        "AINDA EM CONSTRUÇÃO\n"
    )

    return texto


def gerar_bat():
    bat_content_install = """@echo off
        echo =========================
        echo   Instalando o python
        echo =========================
        winget install Python.Python.3.14
        echo =========================
        echo Python instalado
        echo =========================
        
        echo =========================
        echo   Instalando o anki
        echo =========================
	    winget install -e --id Anki.Anki
        echo =========================
        echo Anki instalado
        echo =========================
        
        echo =========================
        echo Instalando pacotes
        echo =========================
        pip install requests
        echo =========================
        echo Pacotes instalados
        echo =========================
        
        echo.
        echo Concluido!
        pause"""
    bat_content = """@echo off
        echo =========================
        echo   LAPIS - Anki Sender
        echo =========================

        python add_card.py

        echo.
        echo Concluido!
        pause"""
    return bat_content, bat_content_install


def gerar_py():
    return """import requests
import os

ANKI_URL = "http://localhost:8765"
DECK_NAME = "Lapis"
MODEL_NAME = "Lapis"

def add_card(palavra, traducao, frase):
    data = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": DECK_NAME,
                "modelName": MODEL_NAME,
                "fields": {
                    "Expression": palavra,
                    "Meaning": traducao,
                    "Sentence": frase
                },
                "tags": ["lapis"]
            }
        }
    }

    response = requests.post(ANKI_URL, json=data)
    return response.json()


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_txt = os.path.join(base_dir, "frases.txt")

    if not os.path.exists(caminho_txt):
        print("Arquivo palavras.txt não encontrado!")
        return

    enviados = 0

    with open(caminho_txt, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()

            if not linha or "-" not in linha or "|" not in linha:
                continue

            try:
                palavra, resto = linha.split("-", 1)
                traducao, frase = resto.split("|", 1)

                palavra = palavra.strip()
                traducao = traducao.strip()
                frase = frase.strip()

                res = add_card(palavra, traducao, frase)

                if res.get("error"):
                    print(f"Erro ao enviar: {linha}")
                else:
                    enviados += 1

            except Exception as e:
                print(f"Erro na linha: {linha}")
                print(e)

    print(f"\\n✅ {enviados} cards enviados!")


if __name__ == "__main__":
    main()
"""
        