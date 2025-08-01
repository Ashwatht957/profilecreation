# 🧑‍💼 Candidate Profile Viewer (Flask + Airtable)

This is a lightweight web app built with **Flask** that dynamically generates candidate profile pages based on records stored in **Airtable**. It includes resume previews, skill listings, and clean profile pages for each candidate.

> ✅ Automatically renders profiles based on Airtable  
> ✅ Preview + download resumes  
> ✅ View all candidates on a single homepage  
> ✅ Easily customizable and extendable

---

## 🚀 Features

- 📋 List all candidates from Airtable on homepage (`/`)
- 🔍 Click a name to view their full profile page (`/profile/<name>`)
- 📎 Preview and download attached resumes
- 🛠 Airtable backend integration via [pyairtable](https://github.com/gtalarico/pyairtable)
- 🧱 Clean code structure with `app.py`, config, and templates
- 🔐 Environment-based API key management with `.env`

---

## 🛠 Tech Stack

- **Backend:** Flask
- **Database:** Airtable
- **Frontend:** HTML + CSS + Jinja2
- **APIs:** pyairtable
- **Deployment:** Run locally or host on Render/Vercel

---

## 📂 Folder Structure

profilecreation/
├── app.py
├── airtable_config.py
├── requirements.txt
├── .env.example
├── templates/
│ ├── home.html
│ └── profile.html