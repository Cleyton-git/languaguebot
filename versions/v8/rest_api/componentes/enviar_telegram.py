import requests

def enviar_telegram(id, msg_id="", msg="", func=""):
    if func == "send_msg":
        requests.post("https://api.telegram.org/bot8249452727:AAExS5DziVnWEUy2kXO-pwFZ5nmhiCt2aBs/sendMessage", json={
                    "chat_id": id,
                    "text": f"{msg}"
                })
    elif func == "send_mp3":
        with open(f"rest_api/componentes/audios/ondoku{msg}.mp3", "rb") as audio:
            requests.post("https://api.telegram.org/bot8249452727:AAExS5DziVnWEUy2kXO-pwFZ5nmhiCt2aBs/sendAudio", data={"chat_id": id}, files={"audio": audio})
                    
        