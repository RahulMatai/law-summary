## 🗄️ Database Schema

```sql
TABLE summaries (
    id          BIGSERIAL PRIMARY KEY,
    session_id  TEXT NOT NULL,        -- isolates data per user
    case_name   TEXT,                 -- extracted by AI
    court       TEXT,                 -- extracted by AI
    summary     JSONB NOT NULL,       -- full structured summary
    created_at  TIMESTAMPTZ DEFAULT NOW()
)
```

### Why JSONB for summary?
- Each summary has 8 fields (facts, issues, reasoning etc.)
- JSONB lets us store all fields in one column
- Easy to query individual fields later if needed
- Flexible — we can add new fields without schema changes