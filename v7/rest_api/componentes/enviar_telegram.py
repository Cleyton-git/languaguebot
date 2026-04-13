import requests

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