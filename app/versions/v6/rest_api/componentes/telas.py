def Tela1():
    print("Bem vindo, escolha uma opção")
    print("[0] - Ver estatisticas")
    print("[1] - Iniciar modo jornada")

def Tela_stats(dados_user):
    print(f"{dados_user[0].palavras} Palavras ja aprendidas")
    print(f"Você ja seguiu a rotina por {dados_user[0].streak} dia")
    