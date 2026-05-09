from . import enviar_telegram
from ..models import Id

def Func_show_keys(tele_id):
    ids = Id.objects.all()
    list_ids = []
    for c in ids:
        list_ids.append(c.id)
    enviar_telegram.enviar_telegram(id=tele_id, msg=f"Keys disponiveis:\n" + "\n".join(list_ids), func="send_msg")
    return