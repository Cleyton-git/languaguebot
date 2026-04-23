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
    caminho_txt = os.path.join(base_dir, "palavras.txt")

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
        