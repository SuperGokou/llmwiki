<h1 align="center">LLM-WIKI</h1>

<p align="center"><strong>Customer Question Prediction Knowledge Graph powered by Flask + SQLite + Ollama + D3.js</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-API-000000?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/D3.js-Force%20Graph-F68E56?logo=d3.js&logoColor=white" alt="D3.js">
  <img src="https://img.shields.io/badge/Ollama-Local%20LLM-111111" alt="Ollama">
  <img src="https://img.shields.io/badge/Status-Active-22C55E" alt="Status">
</p>

<p align="center">
  <a href="http://127.0.0.1:5000"><strong>Local</strong></a>
  ·
  Deploy with <strong>render.yaml</strong> (see Deploy below).
</p>

---

## Overview

LLM-WIKI is a practical knowledge-operating demo for reverse question generation.  
It ingests knowledge files, extracts knowledge points, predicts customer-facing questions, and visualizes relationships in an interactive force-directed graph.  
The built-in assistant (`Gokou's Bot`) answers based on the current knowledge base through local LLM inference.

## Graph

### System Architecture

```mermaid
graph TD
  U[User Browser] --> FE[UI: templates/graph.html]
  FE --> API[Flask API: app.py]
  API --> DB[(SQLite: data/knowledge.db)]
  API --> OLL[Ollama API]
  OLL --> KM[Knowledge Model]
  OLL --> OM[OCR Model]
  OLL --> CM[Chat Model]
```

### Knowledge Graph Model

```mermaid
graph LR
  A[wiki_articles: article node] -->|article_id| Q[predicted_questions: question node]
```

- **Article Node**: `id=article-{id}` with `title/content/source`
- **Question Node**: `id=question-{id}` with `question/question_type`
- **Edge Rule**: one article maps to many predicted questions via `article_id`

## Features

- Multi-format ingestion: `PDF / DOCX / TXT / MD / CSV / TSV / XLSX / images`
- Knowledge-point extraction + customer question prediction
- D3 interactive graph (drag / zoom / focus highlight)
- Knowledge preview, deletion, pagination, and upload workflow
- Local chatbot with model fallback strategy for robustness

## Repository Structure

```text
.
├─ app.py
├─ init_db.py
├─ requirements.txt
├─ render.yaml
├─ .env.example
├─ data/
│  └─ knowledge.db
├─ knowledge_sources/
├─ static/
│  └─ images/
├─ templates/
│  └─ graph.html
└─ README.md
```

## Quick Start

```bash
pip install -r requirements.txt
ollama pull gemma4:latest
ollama pull deepseek-ocr:latest
ollama pull llama3.2:latest
python init_db.py
python app.py
```

Open: <http://127.0.0.1:5000>

## Environment Variables

### 本地（Ollama）

```env
OLLAMA_API_URL=http://127.0.0.1:11434/api/generate
KNOWLEDGE_MODEL=gemma4:latest
OCR_MODEL=deepseek-ocr:latest
CHAT_MODEL=llama3.2:latest
```

### Render / 云端（OpenAI 兼容 API）

容器内**不能**使用 `127.0.0.1:11434`。请设置：

| 变量 | 说明 |
|------|------|
| `LLM_BACKEND` | 固定为 `openai`（表示走 OpenAI 兼容 `/v1/chat/completions`，不是必须用 OpenAI 公司） |
| `OPENAI_API_BASE` | 提供商 Base URL，须含 `/v1`，例如 Groq：`https://api.groq.com/openai/v1` |
| `OPENAI_API_KEY` | 在 Render **Dashboard → 服务 → Environment** 添加为 Secret，**勿提交仓库** |
| `KNOWLEDGE_MODEL` / `OCR_MODEL` / `CHAT_MODEL` | 与提供商文档一致，例如 Groq：`llama-3.3-70b-versatile` |

也可用 OpenAI（`OPENAI_API_BASE=https://api.openai.com/v1`）、OpenRouter 等。图片/PDF 扫描 OCR 需要**支持视觉**的模型；若 Groq 对当前 `OCR_MODEL` 报不支持图片，请换成该服务商允许的 vision 模型或使用 OpenAI `gpt-4o-mini` 作为 `OCR_MODEL`。

若你在自有服务器上暴露了 **公网 Ollama**（`/api/generate`），也可不设 `LLM_BACKEND`，改为把 `OLLAMA_API_URL` 写成该公网地址，并按需要设置 `API_KEY`。

## Deploy (Render)

1. Push this repo to GitHub.
2. In [Render](https://dashboard.render.com): **New** → **Blueprint** → choose the repo and `render.yaml`.
3. 打开 **Environment**，确认已有 `LLM_BACKEND`、`OPENAI_API_BASE`、三个 `*_MODEL`（蓝图可同步）；**手动新增** `OPENAI_API_KEY`（Groq / OpenAI 等控制台创建密钥）。
4. **Manual Deploy** 或等待自动部署完成后访问服务的 `https://….onrender.com`。

**SQLite on Render:** the default disk is ephemeral; redeploys can reset `data/knowledge.db`. For persistence, use a [Render disk](https://render.com/docs/disks) mounted at your app’s data path, or migrate to Postgres.

## Production Notes

- Keep `.env` private and never commit secrets.
- Production web process uses **Gunicorn** (see `render.yaml`); local dev still uses `python app.py`.
- Optionally set `BIND_HOST=0.0.0.0` and `PORT` when running Flask directly behind a tunnel.
- Ensure Ollama (or compatible API URL) is reachable from the deployed host with the configured models pulled.
