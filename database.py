import os
from supabase import create_client,Client

def get_supabase_client():
    try:
        import streamlit as st
        url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
    except Exception:
        from dotenv import load_dotenv
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)
supabase: Client = get_supabase_client()

def save_summary(session_id,case_name,court, summary):
    #save new summary to databse
    supabase.table("summaries").insert({
        "session_id": session_id,
        "case_name": case_name,
        "court": court,
        "summary": summary,
    }).execute()
    #keep only top 3 per session- delete older ones
    all  = supabase.table("summaries")\
        .select("id")\
        .eq("session_id", session_id)\
        .order("created_at", desc=True)\
        .execute()
        
    if len(all.data) > 3:
        old_ids = [r["id"] for r in all.data[3:]]
        for old_id in old_ids:
            supabase.table("summaries").delete().eq("id", old_id).execute()

def get_recent_summaries(session_id):
    response = supabase.table("summaries")\
        .select("*")\
        .eq("session_id", session_id)\
        .order("created_at", desc=True)\
        .limit(3)\
        .execute()
    return response.data