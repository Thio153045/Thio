def detect_job_level(job_title, job_description=""):
    """
    Simple rule-based detector for job level.
    Returns one of: "Entry Level", "Staff Senior", "Supervisor", "Manager"
    """
    text = (job_title + " " + job_description).lower()

    level_keywords = {
        "Manager": ["merencanakan", "mengelola", "bertanggung jawab", "manajer", "manager", "memimpin tim", "strategi"],
        "Supervisor": ["mengawasi", "supervisor", "mengontrol", "mengevaluasi", "monitoring"],
        "Staff Senior": ["senior", "pengalaman", "mampu memimpin sebagian", "koordinasi"],
        "Entry Level": ["melaksanakan", "membantu", "menjalankan", "asisten", "entry"]
    }

    scores = {k: 0 for k in level_keywords}
    for level, kws in level_keywords.items():
        for kw in kws:
            if kw in text:
                scores[level] += 1

    top = max(scores, key=lambda k: scores[k])
    return top if scores[top] > 0 else "Entry Level"
