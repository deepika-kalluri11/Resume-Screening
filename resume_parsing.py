from IPython import get_ipython
from IPython.display import display
from google.colab import drive
import os
import glob
import pdfplumber
import docx2txt
import pandas as pd
import re

from google.colab import drive
drive.mount('/content/drive')

pip install pdfplumber docx2txt

resume_dir = "/content/drive/MyDrive/Resume"

pdf_files = glob.glob(os.path.join(resume_dir, "*.pdf"))
docx_files = glob.glob(os.path.join(resume_dir, "*.docx"))

def extract_text_from_pdf(pdf_path):
       try:
           text = ""
           with pdfplumber.open(pdf_path) as pdf:
               for page in pdf.pages:
                   text += page.extract_text() + "\n" if page.extract_text() else ""
           return text.strip()
       except Exception as e:
           print(f"Error processing PDF: {pdf_path} - {e}")
           return ""
def extract_text_from_docx(docx_path):
    try:
        text = docx2txt.process(docx_path)
        return text.strip() if text else "Empty file"
    except Exception as e:
        print(f"Error processing DOCX: {docx_path} - {e}")
        return ""

pdf_texts = {}
for pdf_path in pdf_files:
    pdf_texts[os.path.basename(pdf_path)] = extract_text_from_pdf(pdf_path)
docx_texts = {}
for docx_path in docx_files:
    docx_texts[os.path.basename(docx_path)] = extract_text_from_docx(docx_path)

email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
phone_regex = r"\b(?:\+91[-\s]?)?[6789]\d{9}\b"
skills_regex = r'(?:' + '|'.join(re.escape(skill) for skill in keywords) + r')'
def extract_resume_details(text):
    text = text.lower()
    email = re.findall(email_regex, text)
    phone = re.findall(phone_regex, text)
    skills = re.findall(skills_regex, text, re.IGNORECASE)

    return {
        "email": email[0] if email else "Not Found",
        "phone": phone[0] if phone else "Not Found",
        "skills": ', '.join(list(set(skills)))
    }
df["email"] = df["text"].apply(lambda x: extract_resume_details(x)["email"])
df["phone"] = df["text"].apply(lambda x: extract_resume_details(x)["phone"])
df["skills"] = df["text"].apply(lambda x: extract_resume_details(x)["skills"])
display(df[["file_name", "email", "phone", "skills"]].style.set_properties(**{'text-align': 'left'}))

keywords = {
    "Python": 2,
    "Machine Learning": 3,
    "Data Science": 3,
    "SQL": 2
}

def score_resume(text):
    score = 0
    for keyword, weight in keywords.items():
      pattern = r"\b" + re.escape(keyword) + r"\b"
      if re.search(pattern, text, re.IGNORECASE):
            score += weight
    return score

for pdf_path in pdf_files:
    text = extract_text_from_pdf(pdf_path)
    score = score_resume(text)
    resume_scores[os.path.basename(pdf_path)] = score

df["text"] = df["file_name"].map(pdf_texts).fillna(df["file_name"].map(docx_texts))

df["email"] = df["text"].apply(lambda x: extract_resume_details(x)["email"])
df["phone"] = df["text"].apply(lambda x: extract_resume_details(x)["phone"])
df["skills"] = df["text"].apply(lambda x: extract_resume_details(x)["skills"])
df["score"] = df["text"].apply(lambda x: score_resume(x))
display(df[["file_name", "email", "phone", "skills", "score"]].style.set_properties(**{'text-align': 'left'}))

selected_resumes = df[df['score'] >= 8]

display(selected_resumes[["file_name", "email", "phone", "skills", "score"]].style.set_properties(**{'text-align': 'left'}))