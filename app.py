from flask import Flask, render_template, abort
from airtable_config import get_record_by_name, get_all_candidates

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

if __name__ == '__main__':
    app.run(debug=True)
