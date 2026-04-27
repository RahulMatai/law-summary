import uuid
import streamlit as st
import backend as bk
import database as db

st.set_page_config(
    page_title="Court Judgement Summarizer",
    page_icon="⚖️",
    layout="wide"
)

if "session_id" not in st.query_params:
    st.query_params["session_id"] = str(uuid.uuid4())

session_id = st.query_params["session_id"]

st.title("⚖️ Court Judgement Summarizer")
st.caption("Upload any Indian court judgement and get a structured summary instantly.")

st.subheader("Upload Judgement")

input_method = st.radio("Choose input method", 
    ["Upload PDF", "Paste URL"], 
    horizontal=True)

text = None
if "judgement_text" not in st.session_state:
    st.session_state.judgement_text = None

if input_method == "Upload PDF":
    uploaded_file = st.file_uploader("Upload court judgement PDF", type=["pdf"])
    if uploaded_file:
        with st.spinner("Extracting text from PDF..."):
            text = bk.extract_text_from_pdf(uploaded_file)
            st.session_state.judgement_text = text
        st.success(f"✅ Extracted {len(text)} characters from PDF")

elif input_method == "Paste URL":
    url = st.text_input("Paste judgement URL", 
        placeholder="https://indiankanoon.org/doc/...")
    if url:
        with st.spinner("Fetching judgement from URL..."):
            text = bk.extract_text_from_url(url)
            st.session_state.judgement_text = text

        st.success(f"✅ Extracted {len(text)} characters from URL")

if text:
    if st.button("⚖️ Summarize Judgement", use_container_width=True):
        with st.spinner("Analyzing judgement with AI... this may take a moment"):
            summary = bk.summarize_judgement(text)
            db.save_summary(
                session_id=session_id,
                case_name=summary.get("case_name", "Unknown"),
                court=summary.get("court", "Unknown"),
                summary=summary
            )

            st.success("✅ Summary generated!")

            st.markdown(f"## {summary.get('case_name', 'Case Summary')}")
            st.markdown(f"**Court:** {summary.get('court')} | **Date:** {summary.get('date')}")

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📋 Facts of the Case")
                st.write(summary.get("facts"))

                st.markdown("### ❓ Issues Raised")
                st.write(summary.get("issues"))

                st.markdown("### 📜 Procedural History")
                st.write(summary.get("procedural_history"))

            with col2:
                st.markdown("### 🧠 Reasoning & Analysis")
                st.write(summary.get("reasoning"))

                st.markdown("### ⚖️ Ratio Decidendi")
                st.write(summary.get("ratio_decidendi"))

                st.markdown("### 🔨 Final Judgement")
                st.write(summary.get("judgement"))
st.divider()
st.subheader("📚 Recent Summaries")

recent = db.get_recent_summaries(session_id)

#new---------------

# Follow-up questions section
if st.session_state.judgement_text:
    st.divider()
    st.subheader("🔍 Ask a Specific Question")
    st.caption("Want to know more? Ask anything about this judgement.")
    
    question = st.text_input("Your question", 
        placeholder="e.g. Explain the punishment in detail")
    
    if st.button("Ask", use_container_width=True):
        if question.strip():
            with st.spinner("Thinking..."):
                answer = bk.ask_followup(
                    st.session_state.judgement_text, 
                    question
                )
            st.markdown("### 💡 Answer")
            st.write(answer)
        else:
            st.warning("Please type a question first!")


#---------------new

if not recent:
    st.info("No recent summaries yet. Upload a judgement above!")
else:
    for r in recent:
        with st.expander(f"⚖️ {r['case_name']} — {r['court']}"):
            s = r["summary"]
            st.markdown(f"**Date:** {s.get('date')}")
            st.markdown(f"**Facts:** {s.get('facts')}")
            st.markdown(f"**Issues:** {s.get('issues')}")
            st.markdown(f"**Ratio Decidendi:** {s.get('ratio_decidendi')}")
            st.markdown(f"**Judgement:** {s.get('judgement')}")