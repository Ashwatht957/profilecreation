from flask import Flask, render_template, abort,request
from airtable_config import get_record_by_name, get_all_candidates
from datetime import datetime

app = Flask(__name__)

# Converts name to URL-friendly slug
def slugify(name):
    return name.strip().lower().replace(" ", "-")

# Converts slug back to name
def deslugify(slug):
    return slug.replace("-", " ").title()

# Home page - list all candidates
@app.route('/')
def home():
    records = get_all_candidates()
    candidates = []

    for record in records:
        fields = record.get('fields', {})
        name = fields.get('Candidate Name')
        if name:
            candidates.append({
                'name': name,
                'slug': slugify(name),
                'title': fields.get('Title', 'N/A'),
                'location': fields.get('Location', 'N/A')
            })

    return render_template("home.html", candidates=candidates)

# Profile page - detailed view of one candidate
@app.route('/profile/<slug>')
def profile(slug):
    name = deslugify(slug)
    record = get_record_by_name(name)

    if not record:
        abort(404)

    data = record.get("fields", {})
    created_time = record.get("createdTime", "Unknown")

    if created_time != "Unknown":
        try:
            created_time = datetime.strptime(created_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            created_time = created_time.strftime("%B %d, %Y")
        except ValueError:
            created_time = "Invalid Format"

    return render_template("profile.html", data=data, created_time=created_time)

# Debug route to show raw JSON
@app.route('/debug/<slug>')
def debug(slug):
    name = deslugify(slug)
    record = get_record_by_name(name)
    return record or {"error": "No record found."}

@app.route('/parse-resume', methods=['POST'])
def parse_resume():
    import requests, zipfile, io
    from airtable_config import update_record
    from resume_parser import parse_resume_pdf

    data = request.json
    zip_url = data.get("zip_url")
    record_id = data.get("record_id")

    if not zip_url or not record_id:
        return {"error": "Missing zip_url or record_id"}, 400

    try:
        response = requests.get(zip_url)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            for file in z.namelist():
                if file.endswith(".pdf"):
                    with z.open(file) as pdf_file:
                        pdf_bytes = pdf_file.read()
                        parsed_data = parse_resume_pdf(pdf_bytes)

                        # Update Airtable
                        update_record(record_id, parsed_data)

                        return {"status": "✅ Resume parsed", "parsed_data": parsed_data}, 200

        return {"error": "No PDF found in ZIP"}, 400

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

