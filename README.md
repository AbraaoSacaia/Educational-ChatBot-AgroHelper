# 🌱 AgroHelper - Chatbot Educacional

Chatbot educacional baseado em LLM, com foco em Agricultura, feito em Python.

## Instalação
```bash
pip install -r requirements.txt
```

## Rodar no terminal (Ollama)
```bash
python agrohelper.py
```

## Rodar versão web (Streamlit + Ollama)
```bash
streamlit run app.py
```

### Dicas
- Instale e rode o servidor Ollama local (`ollama serve`) e garanta que um modelo exista (por exemplo `ollama pull llama3.1`).
- Defina `OLLAMA_MODEL` no `.env` para a versão terminal ou selecione o modelo na barra lateral do Streamlit.
- Na barra lateral, ajuste temperatura e tokens máximos.
- Envie arquivos `.txt` e `.pdf` para compor uma base de conhecimento que será usada como contexto nas respostas.
- Use o botão "Limpar conversa" para reiniciar o chat e "Limpar base" para esvaziar o contexto carregado.

## Comandos no terminal
- `sair` → encerra o chatbot
- `quiz` → inicia perguntas de teste
- `carregar arquivo.txt` → adiciona base de conhecimento
- `carregarpdf arquivo.pdf` → adiciona PDF à base
