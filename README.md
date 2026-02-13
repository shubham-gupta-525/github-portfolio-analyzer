# 🚀 GitHub Portfolio Analyzer

An AI-powered Django web application that evaluates GitHub profiles and generates a recruiter-focused portfolio score.

Built for Hackathon 2026.

---

## 🎥 Live Demo Video

Watch the working demo here:

👉 https://drive.google.com/file/d/1cTyaPzjsc3nMwvoYuPVfgkYt8eFf9JOp/view?usp=sharing

---



## 📌 Problem Statement

Many students have GitHub profiles but don’t know:

- How recruiters evaluate them
- What makes a profile strong or weak
- Which projects to improve
- How to stand out in hiring

This tool analyzes public GitHub data and provides structured, recruiter-style insights.

---

## 🧠 Features

- ✅ GitHub Portfolio Score (0–100)
- ✅ Documentation Quality Analysis
- ✅ Activity Consistency Evaluation
- ✅ Impact Measurement (Stars & Engagement)
- ✅ Technical Depth (Language Diversity)
- ✅ Profile Completeness Check
- ✅ Dynamic Actionable Recommendations
- ✅ Recruiter Insight Section
- ✅ Top Projects Highlight
- ✅ Downloadable PDF Report
- ✅ Modern Neon 3D UI

---

## 🛠 Tech Stack

- Python
- Django
- Bootstrap
- GitHub REST API
- ReportLab (PDF Generation)
- Gunicorn (Production Server)
- Render (Deployment)

---

## ⚙️ How It Works

1. User enters GitHub profile URL
2. Application fetches public repository data
3. System analyzes:
   - README coverage
   - Repository activity
   - Stars & impact
   - Language diversity
   - Profile metadata
4. Generates:
   - Structured score breakdown
   - Recruiter insights
   - Personalized recommendations
5. User can download detailed PDF report

---

## 💻 How to Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/github-portfolio-analyzer.git
cd github-portfolio-analyzer
2️⃣ Create Virtual Environment
bash
Copy code
python -m venv venv
Activate:

Windows:

bash
Copy code
venv\Scripts\activate
Mac/Linux:

bash
Copy code
source venv/bin/activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Create .env File
Create a file named:

bash
Copy code
.env
Add:

ini
Copy code
GITHUB_TOKEN=your_github_token_here
5️⃣ Run Migrations
bash
Copy code
python manage.py migrate
6️⃣ Start Server
bash
Copy code
python manage.py runserver
Open:

cpp
Copy code
http://127.0.0.1:8000/