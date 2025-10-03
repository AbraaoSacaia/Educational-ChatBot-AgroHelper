# AgroHelper - Versão Terminal
import os, time
import openai
from dotenv import load_dotenv
import PyPDF2

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-3.5-turbo"
SYSTEM_PROMPT = "Você é AgroHelper, um assistente educacional sobre agricultura. Responda com clareza, simplicidade e de forma didática. Só deves responder apenas perguntas sobre agricultura e mais nada"

session_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
knowledge_base = []

def ask_llm(user_text: str, max_tokens: int = 200):
    # Palavras-chave relacionadas à agricultura
    keywords = [
        "agricultura", "planta", "solo", "fertilizante", "colheita", "praga", "irrigação", "cultivo",
        "semente", "adubo", "agro", "pecuária", "horta", "agropecuária", "produtor", "fazenda", "rural",
        "agronomia", "agroquímico", "agricultor", "trator", "plantio", "pesticida", "agroindústria"
    ]
    if not any(k in user_text.lower() for k in keywords):
        return "Só consigo fornecer informações relacionadas à agricultura. Perguntas fora desse contexto não serão respondidas."
    session_messages.append({"role": "user", "content": user_text})
    try:
        resp = openai.chat.completions.create(
            model=MODEL,
            messages=session_messages,
            max_tokens=max_tokens,
            temperature=0.2,
        )
        answer = resp.choices[0].message.content.strip()
        session_messages.append({"role": "assistant", "content": answer})
        return answer
    except Exception as e:
        return f"Erro: {e}"

def main():
    print("🌱 AgroHelper iniciado. Digite 'sair' para encerrar.")
    while True:
        user = input("Você: ")
        if user.lower() == "sair":
            print("AgroHelper: Até logo!")
            break
        resposta = ask_llm(user)
        print("AgroHelper:", resposta)

if __name__ == "__main__":
    main()
