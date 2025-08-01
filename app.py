import os
import requests
import zipfile
import tempfile
from flask import Flask, request, render_template, abort, jsonify
from airtable_config import get_record_by_name, get_all_candidates, update_record_fields
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

def slugify(name):
    return name.strip().lower().replace(" ", "-")

def deslugify(slug):
    return slug.replace("-", " ").title()

# Home page — list all candidates
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

# Candidate profile page
@app.route('/profile/<slug>')
def profile(slug):
    name = deslugify(slug)
    record = get_record_by_name(name)

    if not record:
        abort(404)

    data = record.get("fields", {})
    created_time = record.get("createdTime", "Unknown")
    return render_template("profile.html", data=data, created_time=created_time)

# Debug endpoint for testing a specific record
@app.route('/debug/<slug>')
def debug(slug):
    name = deslugify(slug)
    record = get_record_by_name(name)
    return record or {"error": "No record found."}

# Webhook endpoint for Make.com to parse resume from uploaded ZIP
@app.route('/parse-resume', methods=['POST'])
def parse_resume():
    data = request.get_json()
    zip_url = data.get("zip_url")
    record_id = data.get("record_id")

    if not zip_url or not record_id:
        return jsonify({"error": "Missing zip_url or record_id"}), 400

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, 'resume.zip')
            response = requests.get(zip_url)
            if response.status_code != 200:
                return jsonify({"error": "Failed to download ZIP file"}), 400

            # Save ZIP
            with open(zip_path, 'wb') as f:
                f.write(response.content)

            # Extract ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
                # Look for any PDF or TXT file
                resume_file = next((f for f in zip_ref.namelist() if f.endswith(('.txt', '.pdf'))), None)

            if not resume_file:
                return jsonify({"error": "No valid resume file (.pdf/.txt) found in ZIP"}), 400

            extracted_path = os.path.join(tmpdir, resume_file)

            # Dummy data for now — simulate parsed resume
            parsed_data = {
                "Candidate Name": "Parsed Name",
                "Email Address": "parsed@example.com",
                "Skills": "Python, Flask, REST APIs"
            }

            update_record_fields(record_id, parsed_data)

        return jsonify({"message": "✅ Resume parsed and Airtable record updated!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
