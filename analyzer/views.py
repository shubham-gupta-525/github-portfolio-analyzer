from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import render
from django.conf import settings
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch



import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
} if GITHUB_TOKEN else {}


def index(request):
    if request.method == "POST":
        url = request.POST.get("github_url")

        username = url.rstrip("/").split("/")[-1]

        user_data = analyze_profile(username)

        return render(request, "result.html", user_data)

    return render(request, "index.html")


def analyze_profile(username):

    repos_url = f"https://api.github.com/users/{username}/repos"
    user_url = f"https://api.github.com/users/{username}"

    repos_response = requests.get(repos_url)
    user_response = requests.get(user_url)

    # API Error handling
    if repos_response.status_code != 200:
        return {
            "username": username,
            "score": 0,
            "repos": 0,
            "stars": 0,
            "suggestions": ["Invalid GitHub username or API error."]
        }

    repos = repos_response.json()
    profile_data = user_response.json()

    if not isinstance(repos, list):
        return {
            "username": username,
            "score": 0,
            "repos": 0,
            "stars": 0,
            "suggestions": ["Unexpected API response."]
        }

    total_repos = len(repos)
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)

    repos_with_readme = 0
    recent_updates = 0
    languages = set()

    one_year_ago = datetime.now() - timedelta(days=365)

    for repo in repos:

        # README check
        readme_url = f"https://api.github.com/repos/{username}/{repo['name']}/readme"
        readme_res = requests.get(readme_url)

        if readme_res.status_code == 200:
            repos_with_readme += 1

        # Language tracking
        if repo.get("language"):
            languages.add(repo["language"])

        # Activity check
        if repo.get("updated_at"):
            updated = datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
            if updated > one_year_ago:
                recent_updates += 1

    # -------------------------
    # SCORING SYSTEM
    # -------------------------

    # Documentation Score (0-20)
    documentation_score = int((repos_with_readme / total_repos) * 20) if total_repos > 0 else 0

    # Activity Score (0-20)
    activity_score = int((recent_updates / total_repos) * 20) if total_repos > 0 else 0

    # Impact Score (0-20)
    avg_stars = total_stars / total_repos if total_repos > 0 else 0
    if avg_stars > 500:
        impact_score = 20
    elif avg_stars > 100:
        impact_score = 15
    elif avg_stars > 10:
        impact_score = 10
    else:
        impact_score = 5

    # Technical Depth (0-15)
    diversity_score = min(len(languages) * 3, 15)

    # Profile Completeness (0-15)
    profile_score = 0
    if profile_data.get("bio"):
        profile_score += 5
    if profile_data.get("blog"):
        profile_score += 5
    if profile_data.get("location"):
        profile_score += 5

    total_score = (
        documentation_score +
        activity_score +
        impact_score +
        diversity_score +
        profile_score
    )

    # -------------------------
    # DYNAMIC SUGGESTIONS
    # -------------------------

    suggestions = generate_suggestions(
        total_repos,
        total_stars,
        repos_with_readme,
        recent_updates,
        languages,
        profile_data
    )

    # Top 3 repos
    top_repos = sorted(
        repos,
        key=lambda x: x.get("stargazers_count", 0),
        reverse=True
    )[:3]
    print("Repos Status:", repos_response.status_code)
    print("Repos Response:", repos_response.json())

    return {
        "username": username,
        "score": total_score,
        "repos": total_repos,
        "stars": total_stars,
        "documentation_score": documentation_score,
        "activity_score": activity_score,
        "impact_score": impact_score,
        "diversity_score": diversity_score,
        "profile_score": profile_score,
        "suggestions": suggestions,
        "top_repos": top_repos
    }
    


def generate_suggestions(total_repos, total_stars, repos_with_readme,
                         recent_updates, languages, profile_data):

    suggestions = []

    #  1. Repository Count Check
    if total_repos < 5:
        suggestions.append("Add more meaningful projects to demonstrate consistency.")

    #  2. README Coverage Check
    if total_repos > 0:
        readme_ratio = repos_with_readme / total_repos
        if readme_ratio < 0.5:
            suggestions.append("Improve README files. Add installation steps, features, and screenshots.")

    #  3. Impact Check
    avg_stars = total_stars / total_repos if total_repos > 0 else 0
    if avg_stars < 5:
        suggestions.append("Build real-world or impactful projects to increase visibility and stars.")

    #  4. Activity Check
    if total_repos > 0:
        activity_ratio = recent_updates / total_repos
        if activity_ratio < 0.4:
            suggestions.append("Increase contribution consistency. Recruiters value recent activity.")

    #  5. Language Diversity Check
    if len(languages) <= 1:
        suggestions.append("Expand your technical depth by exploring multiple programming languages.")

    #  6. Profile Completeness
    if not profile_data.get("bio"):
        suggestions.append("Add a professional bio to your GitHub profile.")

    if not profile_data.get("blog"):
        suggestions.append("Add portfolio or LinkedIn link to your GitHub profile.")

    #  7. Pinned Projects (Always Useful)
    suggestions.append("Pin your top 3–4 strongest projects on your GitHub profile.")

    return suggestions[:5]


def download_pdf(request, username):

    data = analyze_profile(username)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{username}_github_report.pdf"'

    doc = SimpleDocTemplate(response)
    elements = []

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["Normal"]

    # -----------------------
    # TITLE
    # -----------------------
    elements.append(Paragraph("GitHub Portfolio Analysis Report", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    # -----------------------
    # USER INFO
    # -----------------------
    elements.append(Paragraph(f"<b>Username:</b> {data['username']}", normal_style))
    elements.append(Paragraph(f"<b>Total Score:</b> {data['score']}/100", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # -----------------------
    # SCORE BREAKDOWN
    # -----------------------
    elements.append(Paragraph("Score Breakdown", heading_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Documentation: {data.get('documentation_score', 0)}/20", normal_style))
    elements.append(Paragraph(f"Activity: {data.get('activity_score', 0)}/20", normal_style))
    elements.append(Paragraph(f"Impact: {data.get('impact_score', 0)}/20", normal_style))
    elements.append(Paragraph(f"Technical Depth: {data.get('diversity_score', 0)}/15", normal_style))
    elements.append(Paragraph(f"Profile Completeness: {data.get('profile_score', 0)}/15", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # -----------------------
    # PROFILE STATS
    # -----------------------
    elements.append(Paragraph("Profile Statistics", heading_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Total Repositories: {data['repos']}", normal_style))
    elements.append(Paragraph(f"Total Stars: {data['stars']}", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # -----------------------
    # RECOMMENDATIONS
    # -----------------------
    elements.append(Paragraph("Actionable Recommendations", heading_style))
    elements.append(Spacer(1, 0.2 * inch))

    suggestions = data.get("suggestions", [])
    suggestion_items = [ListItem(Paragraph(s, normal_style)) for s in suggestions]
    elements.append(ListFlowable(suggestion_items, bulletType='bullet'))
    elements.append(Spacer(1, 0.3 * inch))

    # -----------------------
    # RECRUITER INSIGHT
    # -----------------------
    elements.append(Paragraph("Recruiter Insight", heading_style))
    elements.append(Spacer(1, 0.2 * inch))

    score = data.get("score", 0)

    if score > 75:
        insight = "Strong profile. Shows impact and consistency."
    elif score > 50:
        insight = "Moderate profile. Improve documentation and impact."
    else:
        insight = "Needs improvement. Add better projects and README files."

    elements.append(Paragraph(insight, normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # -----------------------
    # TOP PROJECTS
    # -----------------------
    elements.append(Paragraph("Top Projects", heading_style))
    elements.append(Spacer(1, 0.2 * inch))

    top_repos = data.get("top_repos", [])

    if top_repos:
        for repo in top_repos:
            repo_line = f"{repo.get('name')} (⭐ {repo.get('stargazers_count', 0)})"
            elements.append(Paragraph(repo_line, normal_style))
    else:
        elements.append(Paragraph("No top projects available.", normal_style))

    # Build PDF
    doc.build(elements)

    return response