from PyPDF2 import PdfReader
import io
import re

def parse_resume_pdf(pdf_bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Basic email + name extraction
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    name = text.split('\n')[0].strip()  # crude name guess

    skills = []
    if "python" in text.lower(): skills.append("Python")
    if "sql" in text.lower(): skills.append("SQL")
    if "java" in text.lower(): skills.append("Java")

    return {
        "Candidate Name": name,
        "Email Address": email.group() if email else "N/A",
        "Skills": ", ".join(skills) if skills else "N/A"
    }
