import re
from PyPDF2 import PdfReader

def parse_resume_file(file_path):
    data = {
        "Candidate Name": "N/A",
        "Email Address": "N/A",
        "Skills": "N/A",
        "Experience": "N/A"
    }

    try:
        reader = PdfReader(file_path)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

        # Name
        name_match = re.search(r'Name[:\s]+(.+)', text, re.I)
        if name_match:
            data["Candidate Name"] = name_match.group(1).strip()

        # Email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            data["Email Address"] = email_match.group(0)

        # Skills (demo logic, improve later)
        skills = []
        for skill in ["Python", "Java", "SQL", "Excel", "JavaScript"]:
            if skill.lower() in text.lower():
                skills.append(skill)
        data["Skills"] = ", ".join(skills) if skills else "N/A"

        # Experience (simple years logic)
        exp_match = re.search(r'(\d+)\+?\s+years? experience', text, re.I)
        if exp_match:
            data["Experience"] = exp_match.group(1) + " years"

    except Exception as e:
        print(f"Resume parsing error: {e}")

    return data
