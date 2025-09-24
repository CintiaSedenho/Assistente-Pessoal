import openai
import json
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# Carrega o perfil do usuário
with open("perfil_usuario.txt", "r", encoding="utf-8") as f:
    perfil = f.read()

# Tenta carregar o histórico anterior
try:
    with open("historico.json", "r", encoding="utf-8") as f:
        historico = json.load(f)
except FileNotFoundError:
    historico = []

# Adiciona o sistema com o perfil do usuário
mensagens = [{"role": "system", "content": f"Você é uma assistente pessoal da Ana. {perfil}"}]
mensagens += historico

while True:
    entrada = input("Você: ")
    if entrada.lower() in ["sair", "exit", "quit"]:
        break

    mensagens.append({"role": "user", "content": entrada})

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=mensagens
    )

    conteudo = resposta.choices[0].message.content
    print(f"Assistente: {conteudo}")

    mensagens.append({"role": "assistant", "content": conteudo})

    # Salva o histórico da conversa
    with open("historico.json", "w", encoding="utf-8") as f:
        json.dump(mensagens[1:], f, ensure_ascii=False, indent=2)  # Ignora o primeiro (system)
