from ..models import Usuario, FraseUsuario
from django.utils import timezone
from . import enviar_telegram

def Func_remind_users():
    usuarios = Usuario.objects.all()
    for c in usuarios:
        if not c.proximo_estudo:
            continue
        c.reminder_minutes -= 15
        c.save() 
        if 0 < c.reminder_minutes <= 15:
            hora_atual = timezone.localtime()
            tempo_falta = timezone.localtime(c.proximo_estudo)
            diferenca = (tempo_falta - hora_atual)
            minutos = int(diferenca.total_seconds() // 60)
            
            enviar_telegram.enviar_telegram(id=c.telegram_id, msg=(
                                                                    f"⏰ Ei! Faltam {minutos} minutos para o seu horário de estudos.\n"
                                                                    f"\n"
                                                                    f"Bora estudar um pouco de inglês hoje? 🔥"
                                                                    ), func="send_msg")
            
        elif c.reminder_minutes == 0: 
            enviar_telegram.enviar_telegram(id=c.telegram_id, msg=(
                                                                    "🚨 Opa mano… você esqueceu de estudar hoje? 👀\n"
                                                                    "\n"
                                                                    "Ainda dá tempo de manter seu streak vivo 🔥\n"
                                                                    "\n"
                                                                    "Vai lá estudar só um pouquinho."
                                                                    ), func="send_msg")
            c.reminder_minutes = 1440 
            c.save()
        else:
            pass
    return

def Func_remind_jornada():
    usuarios = Usuario.objects.all()
    for c in usuarios:
        frases_usuario = FraseUsuario.objects.filter(usuario__nome_usuario=c.nome_usuario)
        if frases_usuario:
            if c.reminder_jornada == 0:
                enviar_telegram.enviar_telegram(id=c.telegram_id, msg=(
                                                        "🚨 Opa mano… você esqueceu de estudar hoje? 👀\n"
                                                        "\n"
                                                        "Ainda dá tempo de manter seu streak vivo 🔥\n"
                                                        "\n"
                                                        "Vai lá estudar só um pouquinho."), func="send_msg")
                c.reminder_jornada += 1
                c.save()

            elif c.reminder_jornada == 1:
                # Segundo aviso
                enviar_telegram.enviar_telegram(
                    id=c.telegram_id,
                    msg=(
                        "📚 Ei, suas frases ainda estão te esperando.\n"
                        "\n"
                        "Se deixar pra depois, fica bem mais difícil lembrar delas 😵‍💫\n"
                        "\n"
                        "Só alguns minutos já ajudam bastante."
                    ),
                    func="send_msg"
                )
                c.reminder_jornada += 1
                c.save()

            elif c.reminder_jornada == 2:
                # Último aviso
                enviar_telegram.enviar_telegram(
                    id=c.telegram_id,
                    msg=(
                        "⚠️ Último aviso do dia.\n"
                        "\n"
                        "Se você não terminar sua jornada, suas frases pendentes poderão ser removidas ⏳\n"
                        "\n"
                        "Corre lá antes que seja tarde 😭"
                    ),
                    func="send_msg"
                )

                # Resetar depois do último aviso
                c.reminder_jornada += 1
                c.save()
            
            elif c.reminder_jornada == 3:
                frases_usuario.delete()
                
                c.reminder_jornada = -1
                c.reminder_minutes = 1440
                c.tela_atual = "logado"
                
                c.palavra_atual = 0
                c. streak = 0
                
                c.save()
