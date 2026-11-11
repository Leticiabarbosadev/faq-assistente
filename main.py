import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from fastapi.responses import FileResponse

load_dotenv()
BASE = Path(__file__).parent

app = FastAPI(title="Assistente de FAQ")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
MODELO = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

FAQ = (BASE / "faq.txt").read_text(encoding="utf-8")

INSTRUCOES = (
    "Você é um assistente de atendimento de um app de delivery. "
    "Responda em português, de forma curta e educada, usando SOMENTE "
    "as informações do FAQ abaixo. "
    "NUNCA use conhecimento geral sobre apps de delivery: se o assunto "
    "não estiver escrito de forma explícita no FAQ, diga que não tem "
    "essa informação e sugira falar com o atendimento. "
    "Não invente regras, prazos ou valores.\n\n"
    "FAQ:\n"
)


@app.get("/", include_in_schema=False)
def pagina():
    return FileResponse(BASE / "index.html")


@app.get("/saude")
def saude():
    return {"status": "ok"}


@app.post("/perguntar")
def perguntar(pergunta: str):
    try:
        resposta = client.chat.completions.create(
            model=MODELO,
            temperature=0,
            messages=[
                {"role": "system", "content": INSTRUCOES + FAQ},
                {"role": "user", "content": pergunta},
            ],
        )
    except Exception as erro:
        raise HTTPException(status_code=502, detail=f"Erro ao chamar o LLM: {erro}")

    return {
        "pergunta": pergunta,
        "resposta": resposta.choices[0].message.content,
    }