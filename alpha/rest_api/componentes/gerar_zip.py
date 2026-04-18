import io
from deep_translator import GoogleTranslator
import zipfile
import genanki
import tempfile, os


def criar_zip(apkg_bytes, frases, incluir_instrucao):
    frases = gerar_txt_frases(frases)
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        zipf.writestr("deck.apkg", apkg_bytes)

        zipf.writestr("palavras.txt", frases.getvalue())

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
        "2. Abra o arquivo .apkg\n"
        "Android:\n"
        "1. Baixe o anki na play/app store\n"
        "2. Clique nos 3 pontos no canto superior direito\n"
        "3. Importar e baralho (.apkg)\n"
        "4. Selecione o .apkg que você baixou)\n"
    )

    buffer.write(texto.encode("utf-8"))
    buffer.seek(0)

    return buffer
