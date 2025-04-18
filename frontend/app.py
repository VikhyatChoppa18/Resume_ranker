import streamlit as st
import requests

st.title("AI Resume Screener System")

jd = st.text_area("Paste the  your Job Description")
files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)

if st.button("Rank Candidates"):
    if not jd or not files:
        st.warning("Upload resumes and provide a job description.")
    else:
        upload_files = [("files", (f.name, f, f.type)) for f in files]
        res = requests.post("http://localhost:8000/rank", files=upload_files, data={"job_description": jd})
        results = res.json()

        if results:
            st.success("Top Candidates:")
            st.dataframe(results)
        else:
            st.info("No qualified candidates found.")
