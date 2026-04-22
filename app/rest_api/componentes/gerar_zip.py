import io
from deep_translator import GoogleTranslator
import zipfile

def criar_zip(frases, incluir_instrucao):
    zip_buffer = io.BytesIO()
    
    palavras_txt = gerar_txt_frases(frases)
    bat_content = gerar_bat()
    py_content = gerar_py()

    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        zipf.writestr("palavras.txt", palavras_txt.getvalue())
        zipf.writestr("run.bat", bat_content)
        zipf.writestr("add_card.py", py_content)

        if incluir_instrucao:
            zipf.writestr("LEIA-ME.txt", gerar_instrucao().getvalue())

    zip_buffer.seek(0)
    return zip_buffer


def gerar_txt_frases(frases_user):
    buffer = io.BytesIO()
    
    conteudo = ""
    for f in frases_user:
        traducao = GoogleTranslator(source='en', target='pt').translate(f.palavra)
        conteudo += f"{f.palavra} - {traducao} | {f.frase}\n"

    buffer.write(conteudo.encode("utf-8"))
    buffer.seek(0)
    return buffer

def gerar_instrucao():
    buffer = io.BytesIO()

    texto = (
        "Como usar o Anki:\n\n"
        "Desktop:\n"
        "1. Baixe o Anki:https://apps.ankiweb.net/\n"
        "2. Baixe um deck padrão: https://ankiweb.net/shared/info/1827837348\n"
        "3. Abra o deck que você baixou\n"
        "4. Instale o anki connect (ctrl+shift+a/obter extensões, coloque esse código -> 2055492159 e reinicie o anki)\n"
        "5. Clique no import.bat\n"
        "6. Após isso, é so clicar no import.bat com o anki aberto todos os dias\n"
        "Android:\n"
        "1. Baixe o anki na play/app store\n"
        "2. Clique nos 3 pontos no canto superior direito\n"
        "3. Importar e baralho (.apkg)\n"
        "4. Selecione o .apkg que você baixou)\n"
    )

    buffer.write(texto.encode("utf-8"))
    buffer.seek(0)

    return buffer


def gerar_bat():
    bat_content = """@echo off
        echo =========================
        echo   LAPIS - Anki Sender
        echo =========================

        python add_card.py

        echo.
        echo Concluido!
        pause"""
    return bat_content


def gerar_py():
    return """import requests

def add_card(front, back):
    url = "http://localhost:8765"
    data = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "LAPIS",
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": ["auto"]
            }
        }
        }
    requests.post(url, json=data)

    with open("palavras.txt", "r", encoding="utf-8") as f:
        for linha in f:
            if "-" in linha:
                palavra, resto = linha.split("-", 1)
                front = palavra.strip()
                back = resto.strip()
                add_card(front, back)

    print("Cards enviados!")
    """
        