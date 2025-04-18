import docx
from PyPDF2 import PdfReader
import spacy
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

def text_extraction(file):
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""

def entities_extr(text):
    doc = nlp(text)
    return {
        "name": next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), "N/A"),
        "orgs": [ent.text for ent in doc.ents if ent.label_ == "ORG"],
        "dates": [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    }

def process_resumes(files, jd_text):
    results = []
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    for f in files:
        text = text_extraction(f)
        if not text: continue
        ent = entities_extr(text)
        emb = model.encode(text, convert_to_tensor=True)
        score = util.pytorch_cos_sim(emb, jd_emb).item()
        if score >= 0.5:
            results.append({
                "name": ent['name'],
                "filename": f.filename,
                "score": round(score, 3),
                "orgs": ent["orgs"],
                "dates": ent["dates"]
            })
    return sorted(results, key=lambda x: x["score"], reverse=True)
