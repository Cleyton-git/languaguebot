# 🧠 LanguageBot

LanguageBot é um bot de estudos de inglês baseado em IA, criado para transformar prática diária em uma experiência de progressão contínua.

O projeto combina:

- Correção automática de frases com IA
- Sistema de streak diária
- Treino de pronúncia (Ondoku)
- Progressão por níveis
- Geração automática de arquivos de estudo
- Integração com Telegram
- Deploy online com cronjob para manter o bot ativo 24/7

---

# 🚀 Funcionalidades

## 🤖 Correção de frases com IA

O usuário envia frases em inglês e a IA:

- Detecta se estão corretas
- Explica erros gramaticais
- Corrige mantendo o significado original
- Retorna tudo em JSON estruturado

Exemplo:

```json
{
  "todas_certas": false,
  "frases": [
    {
      "frase_original": "She go yesterday",
      "status": "❌ Errada",
      "explicacao": "Use 'went' no passado.",
      "correcao": "She went yesterday."
    }
  ]
}
```

---

## 🎧 Sistema de Ondoku

O bot possui um sistema de treino de fala baseado em repetição:

1. Ler o texto em voz alta
2. Ouvir o áudio
3. Ler novamente junto com o áudio

Cada dia estudado aumenta o `level_ondoku` do usuário.

Novos áudios e conteúdos são desbloqueados conforme o progresso.

---

## 📈 Progressão e retenção

O LanguageBot utiliza:

- Sistema de níveis
- Desbloqueio gradual de conteúdo
- Cooldown anti-spam
- Streak diária
- Rotina de 30 dias de estudo

A ideia é incentivar consistência ao invés de apenas uso casual.

---

## 📦 Geração automática de arquivos

Após os estudos, o bot:

- Salva frases corrigidas
- Atualiza dados do usuário
- Gera automaticamente arquivos `.txt`
- Compacta tudo em `.zip`
- Envia os materiais pelo Telegram

---

# ⚙️ Tecnologias utilizadas

## Backend

- Python
- Django
- SQLite
- Threading

## IA

- Gemini API
- OpenRouter

## Integrações

- Telegram Bot API
- Cronjob/Ping Service

---

# 🧩 Arquitetura do projeto

O sistema foi construído em módulos separados:

- Integração com IA
- Controle de usuários
- Sistema de Ondoku
- Sistema de cooldown
- Geração de ZIP/TXT
- Envio de mensagens Telegram
- Controle de progresso

---

# 🛡️ Problemas resolvidos durante o desenvolvimento

Durante o projeto foram resolvidos diversos problemas reais de backend:

- Race conditions com threads
- Timeout de requests
- Queue de respostas da IA
- Parsing de JSON inválido
- Deploy em host gratuita
- Bot entrando em modo sleep
- Rate limit de APIs
- Sistema de cooldown anti-spam
- Erros de migrations do Django

---

# 🌐 Deploy

O bot foi hospedado em uma plataforma gratuita.

Como hosts gratuitas colocam aplicações em modo sleep após um tempo sem atividade, foi criado um sistema com cronjob/ping automático para manter o bot ativo 24 horas por dia.

---

# 📌 Objetivo do projeto

O LanguageBot nasceu com dois objetivos:

1. Melhorar o inglês através de prática diária
2. Aprender backend, deploy, IA e arquitetura de sistemas na prática

---

# 🚧 Status do projeto

✅ Funcional

Atualmente o bot já possui:

- Correção com IA
- Sistema de Ondoku
- Progressão por níveis
- Geração de arquivos
- Deploy online
- Sistema anti-spam
- Cronjob ativo

Novas funcionalidades continuam sendo adicionadas.

---

# 👤 Autor

Desenvolvido por Cleyton Bezerra Miguel
