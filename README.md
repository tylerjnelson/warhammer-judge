# The Judge — Warhammer 40K Rules Adjudicator

A private RAG-powered web app for adjudicating Warhammer 40,000 10th Edition rules.

## Stack
- **LLM**: Groq / qwen/qwen3-32b
- **Vector DB**: ChromaDB (local)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **UI**: Streamlit
- **Auth**: Caddy Basic Auth
- **Data**: Wahapedia CSV exports + HTML scrape

## Setup

### 1. Install dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 3. Run the pipeline
```bash
python scripts/etl.py
python scripts/scrape_rules.py
python scripts/ingest.py
```

### 4. Start the app
```bash
streamlit run app.py --server.port 8501
```

## Architecture
See `warhammer_judge_spec_v6.docx` for full technical specification.
