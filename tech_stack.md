## 🛠️ Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Frontend | Streamlit | Fast, Python native, free hosting |
| AI | Groq API (Llama 3.3 70B) | Free, fast, accurate |
| PDF Parsing | PyPDF | Extract text from court PDFs |
| Database | Supabase (PostgreSQL) | Free, persistent, scalable |
| Hosting | Streamlit Cloud | Free, one click deploy |

## 📁 Project Structure

```
Court-summarizer/
├── app.py              # Streamlit UI
├── backend.py          # Groq AI + PDF/URL extraction
├── database.py         # Supabase DB layer
├── requirements.txt    # Dependencies
├── .env                # Local secrets (gitignored)
├── SYSTEM_DESIGN.md    # Architecture decisions
├── DECISIONS.md        # Design decisions & tradeoffs
└── tests/
    └── test_backend.py # Unit tests
```