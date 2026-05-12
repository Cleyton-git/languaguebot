import requests
from dotenv import load_dotenv
import os
from datetime import date

TOKEN_LOCAL = os.getenv("TOKEN_TELEGRAM_LOCAL")
TOKEN_PROD = os.getenv("TOKEN_TELEGRAM_PROD")
print("TOKEN_PROD -> ", TOKEN_PROD)

### COISAS PARA MUDAR 
def enviar_telegram(id, msg_id="", msg="", func="", file=""):
    if func == "send_msg":
        response = requests.post(f"https://api.telegram.org/bot{TOKEN_PROD}/sendMessage", json={
                    "chat_id": id,
                   "text": f"{msg}"
                })
        print(response.text)
    elif func == "send_mp3":
        with open(f"rest_api/componentes/audios/ondoku{msg}.mp3", "rb") as audio:
            requests.post(f"https://api.telegram.org/bot{TOKEN_PROD}/sendAudio", data={"chat_id": id}, files={"audio": audio})
    
    elif func == "send_zip":
        data = date.today()
        requests.post(f"https://api.telegram.org/bot{TOKEN_PROD}/sendDocument",
                      data={"chat_id": id},
                      files={ "document": ( f"dia{data.day}-{data.month}-{data.year}.zip", file)})
                    
        