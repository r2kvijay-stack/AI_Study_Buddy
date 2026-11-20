import streamlit as st
from google import genai
from pypdf import PdfReader

st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")

st.markdown("<h1 style='text-align:center; color:#6C63FF;'>📚 AI Study Buddy</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Paste Notes → Get Summary + Quiz + Key Terms in 10 Seconds</p>", unsafe_allow_html=True)
st.divider()

st.sidebar.header("⚙️ Setup")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
st.sidebar.info("Free key from aistudio.google.com")
difficulty = st.sidebar.selectbox("Quiz Difficulty", ["Easy", "Medium", "Hard"])

st.subheader("1. Add Your Notes")
tab1, tab2 = st.tabs(["✍️ Paste Notes", "📄 Upload PDF"])
notes_text = ""
with tab1:
    notes_text = st.text_area("Paste your chapter / notes here:", height=200, placeholder="Paste notes here...")
with tab2:
    uploaded = st.file_uploader("Upload Notes PDF", type=["pdf"])
    if uploaded:
        reader = PdfReader(uploaded)
        notes_text = ""
        for page in reader.pages:
            notes_text += page.extract_text() or ""
        st.success("PDF Read Successfully!")

if st.button("🚀 Generate Revision Pack", use_container_width=True):
    if not api_key:
        st.error("Please enter Gemini API Key in sidebar!")
    elif len(notes_text.strip()) < 50:
        st.warning("Please paste at least 50 characters of notes.")
    else:
        with st.spinner("AI is making your revision pack..."):
            client = genai.Client(api_key=api_key)
            prompt = f"""You are Study Buddy for B.Tech students.
            Notes: {notes_text[:8000]}
            Difficulty: {difficulty}
            Give output in EXACT format:
            ## 📝 SUMMARY (5-6 bullet points in simple English)
            ## ❓ 5 MCQs (Each with 4 options A,B,C,D and Correct Answer)
            ## 🔑 3 KEY TERMS (Term - Simple Meaning in 1 line)
            Keep language very simple."""
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            st.success("Done! Your Revision Pack is Ready 👇")
            st.markdown(response.text)
            st.download_button("⬇️ Download Revision Notes", response.text, file_name="revision_notes.txt")

st.divider()
st.markdown("<p style='text-align:center;'>Input → Gemini AI → Summary + Quiz + Key Terms</p>", unsafe_allow_html=True)
