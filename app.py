import os
import requests
import zipfile
import tempfile
from flask import Flask, render_template, abort, request, jsonify
from airtable_config import get_record_by_name, get_all_candidates, update_record_fields
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

def slugify(name):
    return name.strip().lower().replace(" ", "-")

def deslugify(slug):
    return slug.replace("-", " ").title()

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
                'slug': slugify(name)
            })

    return render_template("home.html", candidates=candidates)

@app.route('/profile/<slug>')
def profile(slug):
    name = deslugify(slug)
    record = get_record_by_name(name)

    if not record:
        abort(404)

    data = record.get("fields", {})
    created_time = record.get("createdTime", "Unknown")
    return render_template("profile.html", data=data, created_time=created_time)

@app.route('/debug/<slug>')
def debug(slug):
    name = deslugify(slug)
    record = get_record_by_name(name)
    return record or {"error": "No record found."}

@app.route('/parse-resume', methods=['POST'])
def parse_resume():
    data = request.json
    zip_url = data.get("zip_url")
    record_id = data.get("record_id")

    if not zip_url or not record_id:
        return {"error": "Missing zip_url or record_id"}, 400

    try:
        # Download ZIP file
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, 'resume.zip')
            response = requests.get(zip_url)
            with open(zip_path, 'wb') as f:
                f.write(response.content)

            # Extract contents
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
                resume_file = next((f for f in zip_ref.namelist() if f.endswith('.txt') or f.endswith('.pdf')), None)

            if not resume_file:
                return {"error": "No valid resume file found in ZIP."}, 400

            extracted_path = os.path.join(tmpdir, resume_file)

            # Simulate parsed content
            parsed_data = {
                "Candidate Name": "Parsed Name",
                "Email Address": "parsed@example.com",
                "Skills": "Python, Flask"
            }

            update_record_fields(record_id, parsed_data)

        return {"message": "✅ Resume parsed and record updated!"}, 200

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
