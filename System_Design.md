# System Design — Court Judgement Summarizer

## Problem Statement
Law students in India deal with hundreds of court judgements daily.
Reading full judgements is time consuming. This tool summarizes them instantly.

## User Story
As a law student, I want to upload a PDF or paste a URL of a court judgement
so that I get a structured summary instantly without reading 100+ pages.

## Target Users
- Law students
- Lawyers
- Researchers
- Journalists

## Input Methods
- PDF upload
- URL paste (Indian court URLs)

## Output — Structured Summary
1. Case Name & Citation
2. Court & Date
3. Facts of the Case
4. Issues Raised
5. Procedural History
6. Reasoning & Analysis
7. Ratio Decidendi
8. Final Judgement & Punishment

## Storage Strategy
- Save only last 3 summaries per session
- Text only — no PDFs stored
- Supabase free tier (500MB limit — safely handles ~500,000 summaries)

## Tech Stack
| Layer | Choice |
|-------|--------|
| Frontend | Streamlit |
| AI | Google Gemini API (free) |
| PDF Parsing | PyPDF2 |
| Database | Supabase |
| Hosting | Streamlit Cloud |

## Flow
1. User opens app → session created
2. User uploads PDF or pastes URL
3. App extracts text from PDF/URL
4. Text sent to Gemini API with structured prompt
5. Gemini returns structured summary
6. Summary displayed to user
7. Saved to Supabase (max 3 per session, oldest deleted)

## Limitations
- Indian courts only (V1)
- Max PDF size 10MB
- Gemini free tier — 1500 requests/day