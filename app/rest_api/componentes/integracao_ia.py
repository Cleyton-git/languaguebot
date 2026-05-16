from ..models import FraseUsuario
import json
import google.generativeai as genai
from . import enviar_telegram, gerar_zip
import threading
from django.utils import timezone
import os
from dotenv import load_dotenv
import time
import re


load_dotenv()

TOKEN_IA = os.getenv("TOKEN_API")

def Func_integracao_ia(user, frases_user):
    frases = []
    for c in frases_user:
        frases.append(c.frase)
    texto_frases = "\n".join(frases)
    genai.configure(
        api_key=TOKEN_IA
    )
    model = genai.GenerativeModel(
        "models/gemma-4-31b-it"
    )
    prompt = f"""
Corrija as frases abaixo.

REGRAS:
-NÃO pense em voz alta.
-NÃO explique seu raciocínio.
-NÃO faça análises antes da resposta.
-Retorne apenas o JSON final.
- Diga se a frase está correta ou errada.
- Se estiver errada, explique brevemente e corrija.
- Se estiver correta, deixe "explicacao" e "correcao" vazios.
- Mantenha o significado original.
- Responda na mesma ordem das frases.
- RESPONDA APENAS JSON.
- NUNCA use markdown.
- NUNCA use ```json.
- NUNCA escreva texto fora do JSON.
- O JSON deve ser válido.
- NÃO adicione campos extras.
- NÃO escreva comentários.
- NÃO use vírgulas sobrando.
- Use exatamente os nomes dos campos mostrados abaixo.
- NÃO mude a estrutura do JSON.
- Se a frase estiver correta, mantenha a correção vazia.
-Não escreva nenhum pensamento, análise ou explicação antes do JSON NEM DEPOIS.

FORMATO OBRIGATÓRIO:

{{
    "todas_certas": false,

    "frases": [
        {{
            "frase_original": "She go yesterday",

            "status": "❌ Errada",

            "explicacao": "Use 'went' no passado.",

            "correcao": "She went yesterday."
        }},

        {{
            "frase_original": "I like pizza.",

            "status": "✅ Correta",

            "explicacao": "",

            "correcao": ""
        }}
    ]
}}
    FRASES PARA CORRIGIR:
    {texto_frases}"""
    try:
        response = model.generate_content(prompt)
    except Exception as e:
        print(e)
        enviar_telegram.enviar_telegram(
            id=user.telegram_id,
            msg="⏳ Você entrou em uma fila de espera. Vamos tentar novamente em 1 minuto.",
            func="send_msg"
        )
        #time.sleep(60)
        try:
            enviar_telegram.enviar_telegram(
                id=user.telegram_id,
                msg="⏳ Tentando denovo...",
                func="send_msg"
            )
            response = model.generate_content(prompt, generation_config={ "temperature": 0})

        except Exception:
            enviar_telegram.enviar_telegram(
                id=user.telegram_id,
                msg="⚠️ A IA ainda está ocupada. Tente novamente mais tarde. (Espero uns 5 minutos e reenvie qualquer mensagem)",
                func="send_msg"
            )
            return
    response = response.text
    inicio = response.rfind('{\n    "todas_certas"')

    if inicio == -1:
        inicio = response.rfind('{"todas_certas"')

    json_limpo = response[inicio:]
    print(json_limpo)
    try:
        data = json.loads(json_limpo)
    except Exception as e:
        print(f"LOG -> ERRO_IA {e}")
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg="A ia teve problemas processando... reprocessando", func="send_msg")
        response = model.generate_content(prompt, generation_config={ "temperature": 0})
        response = response.text
        matches = re.findall(r'\{[\s\S]*\}', response)
        json_limpo = matches[-1]
        try:
            data = json.loads(json_limpo)
        except Exception as e:
            print(f"LOG -> ERRO_IA {e}")
            enviar_telegram.enviar_telegram(id=user.telegram_id, msg="A ia teve problemas processando suas frases, espere 30 segundos e envie qualquer coisa", func="send_msg")
            return
    
    if data['todas_certas']:
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg="🏆 Detectei que você acertou TODAS as frases!\n\nParabéns, mandou muito bem 😎🔥", func="send_msg")
    else:
        for c in data['frases']:
            if "Errada" in c["status"]:
                enviar_telegram.enviar_telegram(id=user.telegram_id, 
                                            msg=
                                            f"📚 Sua frase: {c["frase_original"]}\n"
                                            f"📌 Status:{c["status"]}\n"
                                            f"💡 Explicação:{c["explicacao"]}\n"
                                            f"✍️ Correção:{c["correcao"]}\n", func="send_msg")
                frase = FraseUsuario.objects.get(frase=c["frase_original"])
                frase.frase = c['correcao']
                print(frase)
                frase.save()
        enviar_telegram.enviar_telegram(id=user.telegram_id, msg="🤖 Suas frases foram analisadas e corrigidas com sucesso!", func="send_msg")

    enviar_telegram.enviar_telegram(id=user.telegram_id, msg=("📦 Sua pasta está sendo preparada...\n\n""Isso pode levar alguns segundos dependendo da quantidade de frases."),
                                                            func="send_msg")
    frases_user = FraseUsuario.objects.filter(usuario=user).all()
    print(frases_user)
    if user.streak == 0:
        threading.Thread(
        target=gerar_zip.criar_zip,
        args=(user, frases_user, True),
        daemon=True
        ).start()
    else:
        threading.Thread(
        target=gerar_zip.criar_zip,
        args=(user, frases_user, False),
        daemon=True
        ).start()
        
    return
    FraseUsuario.objects.filter(usuario=user.telegram_id).delete()
    user.tela_atual = "descanso"
    user.proximo_estudo = timezone.now() + timedelta(hours=24)

    user.reminder_minutes = 1440
    user.reminder_jornada = -1

    user.palavra_atual = 0
    user.streak += 1
    user.save()

