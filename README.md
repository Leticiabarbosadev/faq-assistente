# Assistente de FAQ para delivery

**Demo online:** https://faq-assistente.onrender.com/
> A primeira abertura pode demorar cerca de 30 segundos, porque o servidor gratuito "dorme" quando fica sem uso.

API e interface de chat que respondem dúvidas de atendimento de um app de delivery (atrasos, cancelamentos, reembolsos, cupons) usando um LLM, **apenas com base em um FAQ**. Quando a resposta não está no FAQ, o assistente diz que não sabe em vez de inventar.


> Projeto de portfólio. O FAQ (`faq.txt`) é fictício e foi escrito por mim.

## Como funciona

```
Pergunta → API (FastAPI) → prompt = instruções + FAQ → LLM (Groq) → resposta
```

- O `faq.txt` é lido na inicialização e enviado ao modelo junto com as instruções (system prompt).
- As instruções obrigam o modelo a responder somente com o conteúdo do FAQ e a encaminhar ao atendimento quando a informação não existir.
- `temperature=0` para respostas mais estáveis.
- A interface (`index.html`) é servida pela própria API.

## Tecnologias

Python · FastAPI · Uvicorn · OpenAI SDK (compatível com a API do Groq) · modelo `openai/gpt-oss-20b` · HTML, CSS e JavaScript

## Como rodar

1. Clone o repositório e entre na pasta:
   ```bash
   git clone https://github.com/Leticiabarbosadev/faq-assistente.git
   cd faq-assistente
   ```
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv .venv
   # Windows (PowerShell): .\.venv\Scripts\Activate.ps1
   # Mac/Linux: source .venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Copie `.env.example` para `.env` e preencha com a sua chave do [Groq](https://console.groq.com/keys):
   ```
   GROQ_API_KEY=sua_chave
   GROQ_MODEL=openai/gpt-oss-20b
   ```
   Para ver quais modelos a sua conta pode usar: `python listar_modelos.py`.
5. Suba o servidor:
   ```bash
   python -m uvicorn main:app --reload
   ```
6. Abra `http://127.0.0.1:8000/` (chat) ou `http://127.0.0.1:8000/docs` (documentação da API).

## Avaliação

O script `avaliar.py` envia perguntas à API e confere se a resposta contém o esperado. Os casos incluem perguntas do FAQ, perguntas com outras palavras, uma pergunta que mistura duas regras, perguntas fora do escopo e uma tentativa de burlar as instruções.

| Rodada | Casos | Acertos | Observação |
|---|---|---|---|
| 1 | 15 | 14 | A falha foi do caso de teste: ele supunha que a taxa de entrega não estava no FAQ, mas estava, e o modelo respondeu corretamente. |
| 2 | 16 | 16 | Caso corrigido e adicionado um teste fora do escopo (criptomoeda). |

Para rodar (com o servidor ligado): `python avaliar.py`.

## Estrutura

```
├── main.py             # API (FastAPI) e chamada ao LLM
├── index.html          # interface de chat
├── faq.txt             # base de conhecimento (fictícia)
├── avaliar.py          # avaliação automática
├── listar_modelos.py   # lista os modelos disponíveis na conta
├── requirements.txt
└── .env.example        # modelo do arquivo de configuração
```

## Limitações e próximos passos

- O FAQ inteiro vai no prompt, o que não escala para documentos grandes. Próximo passo: busca por embeddings (RAG) para enviar ao modelo só os trechos relevantes.
- Os casos de teste foram escritos por mim e a conferência é por palavra-chave, então ela pode aceitar respostas imperfeitas ou rejeitar respostas corretas. Falta testar com perguntas de outras pessoas.
- Cada pergunta é independente: o assistente não guarda o histórico da conversa.
- Ainda não há deploy público.