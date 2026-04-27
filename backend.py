import os
from pypdf import PdfReader
import requests
from io import BytesIO
from groq import Groq

def get_groq_client():
    try:
        import streamlit as st
        key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    except Exception:
        from dotenv import load_dotenv
        load_dotenv()
        key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=key)

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def extract_text_from_url(url):
    response = requests.get(url, timeout=10)
    if "pdf" in response.headers.get("Content-Type", ""):
        reader = PdfReader(BytesIO(response.content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    else:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text().strip()

def summarize_judgement(text):
    client = get_groq_client()

    prompt = f"""
    You are a legal expert. Analyze this Indian court judgement and provide a structured summary.
    
    Return ONLY a JSON object with these exact keys:
    {{
        "case_name": "full case name and citation",
        "court": "name of the court",
        "date": "date of judgement",
        "facts": "facts of the case in simple language",
        "issues": "legal issues raised",
        "procedural_history": "how the case reached this court",
        "reasoning": "court's reasoning and analysis",
        "ratio_decidendi": "ratio decidendi — the legal principle established",
        "judgement": "final judgement and punishment if any"
    }}
    
    Judgement text:
    {text[:8000]}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    import json
    clean = response.choices[0].message.content.strip()
    clean = clean.replace("```json", "").replace("```", "")
    return json.loads(clean)

def ask_followup(text, question):
    client = get_groq_client()
    prompt = f"""
    You are a legal expert. A user has read this Indian court judgement 
    and has a specific question about it.
    
    Answer the question in clear, simple language.
    Be detailed but focused only on what is asked.
    
    Judgement text:
    {text[:8000]}
    
    User question:
    {question}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    
    return response.choices[0].message.content.strip()
