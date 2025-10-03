# AgroHelper - Versão Web (Streamlit)
import os
import io
import ollama
import streamlit as st
from dotenv import load_dotenv
import PyPDF2

load_dotenv()

DEFAULT_MODEL = "gemma3:1b"
SYSTEM_PROMPT = (
    "Você é AgroHelper, um assistente educacional sobre agricultura. "
    "Responda curto, claro e didático. Quando usar contexto enviado pelo usuário, cite-o brevemente."
)

st.set_page_config(page_title="AgroHelper", page_icon="🌱")

# Session state init
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = ""
if "settings" not in st.session_state:
    st.session_state.settings = {
        "model": DEFAULT_MODEL,
        "temperature": 0.2,
        "max_tokens": 200,
    }

# Sidebar: settings and uploads
with st.sidebar:
    st.header("Configurações")
    # Detectar modelos locais do Ollama
    try:
        available_models = [m.get("model") or m.get("name") for m in ollama.list().get("models", [])]
    except Exception:
        available_models = []
    if not available_models:
        available_models = [DEFAULT_MODEL]
    # Priorizar gemma3:1b se estiver disponível
    if "gemma3:1b" in available_models:
        model_index = available_models.index("gemma3:1b")
    else:
        model_index = 0

    model = st.selectbox("Modelo (Ollama)", available_models, index=model_index)
    temperature = st.slider("Temperatura", 0.0, 1.0, st.session_state.settings["temperature"], 0.1)
    max_tokens = st.slider("Máx. tokens", 64, 1000, st.session_state.settings["max_tokens"], 16)

    st.session_state.settings.update({
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
    })

    st.markdown("---")
    st.subheader("Base de Conhecimento")
    uploaded_files = st.file_uploader("Envie TXT ou PDF", type=["txt", "pdf"], accept_multiple_files=True)

    def extract_text_from_pdf(file_bytes: bytes) -> str:
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            pages_text = []
            for page in reader.pages:
                pages_text.append(page.extract_text() or "")
            return "\n".join(pages_text)
        except Exception:
            return ""

    kb_chunks = []
    if uploaded_files:
        for f in uploaded_files:
            if f.type == "text/plain" or f.name.lower().endswith(".txt"):
                kb_chunks.append(f.read().decode("utf-8", errors="ignore"))
            elif f.type == "application/pdf" or f.name.lower().endswith(".pdf"):
                kb_chunks.append(extract_text_from_pdf(f.read()))
        combined = "\n\n".join([c for c in kb_chunks if c])
        if combined:
            st.session_state.knowledge_base = (st.session_state.knowledge_base + "\n\n" + combined).strip()
    if st.button("Limpar base"):
        st.session_state.knowledge_base = ""

    kb_preview = st.session_state.knowledge_base[:600] + ("..." if len(st.session_state.knowledge_base) > 600 else "")
    st.text_area("Prévia", value=kb_preview, height=150)

    st.markdown("---")
    if st.button("Limpar conversa"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

st.title("🌱 AgroHelper - Chatbot Educacional")

# Render chat history (excluding system) UI
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# Chat input + send
user_input = st.chat_input("Digite sua pergunta...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Build contextual system message from knowledge base (truncate for safety)
    context = st.session_state.knowledge_base.strip()
    contextual_messages = list(st.session_state.messages)
    if context:
        max_context_chars = 4000
        context_to_use = context[:max_context_chars]
        contextual_messages.insert(0, {
            "role": "system",
            "content": "Contexto adicional do usuário (base de conhecimento):\n" + context_to_use,
        })

    try:
        # Ollama chat completion
        resp = ollama.chat(
            model=st.session_state.settings["model"],
            messages=contextual_messages,
            options={
                "temperature": st.session_state.settings["temperature"],
                "num_predict": st.session_state.settings["max_tokens"],
            },
        )
        answer = (resp.get("message", {}) or {}).get("content", "").strip() or "(sem resposta)"
    except Exception as e:
        answer = f"Erro ao consultar o Ollama: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(answer)
