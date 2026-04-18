from ..models import Usuario, Id, UsuarioOndoku
from . import enviar_telegram, telas

def cadastro_user(tele_id, req):
    
    if req[0:7] == "/ativar":
        id_exists = Id.objects.filter(id=req[-3:]).first()
        if id_exists:
            Usuario.objects.create(
                telegram_id = tele_id,
                palavra_inicial = 0,
                palavra_atual = 0,
                streak = 0,
                tela_atual = "logado"
            )
            id_exists.delete()
            enviar_telegram.enviar_telegram(id=tele_id, msg="Você usou seu código de ativação do bot, o código expirou", func="send_msg")
            enviar_telegram.enviar_telegram(id=tele_id, msg=("👋 Bem-vindo ao bot!\n\n"
                                            "Aqui você segue um ciclo completo para aprender inglês todos os dias:\n\n"
                                            
                                            "📚 1. Vocabulário + Escrita\n"
                                            "Você recebe palavras novas e cria suas próprias frases com elas.\n\n"
                                            
                                            "🧠 2. Fixação ativa\n"
                                            "Nada de só ler — você pratica escrevendo e usando o inglês de verdade.\n\n"
                                            
                                            "🎧 3. Ondoku (Shadowing)\n"
                                            "Você treina com áudio em 3 etapas para destravar sua fala:\n"
                                            "• Lê sozinho\n"
                                            "• Lê junto com o áudio\n"
                                            "• Lê novamente sem ajuda\n\n"
                                            
                                            "📦 4. Revisão inteligente\n"
                                            "No final, você recebe seu material do dia para revisar no Anki.\n\n"
                                            
                                            "🌍 5. Imersão\n"
                                            "Depois disso, o bot recomenda 1h de conteúdo em inglês para consolidar tudo.\n\n"
                                            
                                            "⏱️ Tudo isso em menos de 10 minutos.\n\n"
                                            "🚀 Digite /jornada para começar"), func="send_msg")
            
        else:
            enviar_telegram.enviar_telegram(id=tele_id, msg="Código invalido, tente novamente", func="send_msg")
    else:
        enviar_telegram.enviar_telegram(id=tele_id, msg="Você deve digitar /ativar e seu código\nEX: /ativar 000", func="send_msg")