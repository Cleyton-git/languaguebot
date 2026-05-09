from ..models import Usuario
from django.utils import timezone
from . import enviar_telegram

def Func_remind_users():
    usuarios = Usuario.objects.all()
    for c in usuarios:
        c.reminder_user -= 15
        c.save() 
        if 0 < c.reminder_user <= 15:
            hora_atual = timezone.localtime()
            tempo_falta = timezone.localtime(c.proximo_estudo)
            diferenca = (tempo_falta - hora_atual)
            minutos = int(diferenca.total_seconds() // 60)
            
            enviar_telegram.enviar_telegram(id=c.telegram_id, msg=(
                                                                    f"⏰ Ei! Faltam {minutos} minutos para o seu horário de estudos.\n"
                                                                    f"\n"
                                                                    f"Bora estudar um pouco de inglês hoje? 🔥"
                                                                    ), func="send_msg")
            
        elif c.reminder_user == 0: 
            enviar_telegram.enviar_telegram(id=c.telegram_id, msg=(
                                                                    "🚨 Opa mano… você esqueceu de estudar hoje? 👀\n"
                                                                    "\n"
                                                                    "Ainda dá tempo de manter seu streak vivo 🔥\n"
                                                                    "\n"
                                                                    "Vai lá estudar só um pouquinho."
                                                                    ), func="send_msg")
            c.reminder_user = 1440 
            c.save()
        else:
            pass
    return