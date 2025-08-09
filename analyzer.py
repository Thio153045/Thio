import sqlite3
import re
from job_level_detector import detect_job_level

DB_PATH = "data/competencies.db"

def analyze_job_description(job_title, job_description):
    """
    Analisis uraian jabatan untuk mendapatkan:
    - Pendidikan terakhir
    - Range usia
    - Range pengalaman
    - Daftar kompetensi teknis & soft
    """
    level = detect_job_level(job_title, job_description)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT education, age_min, age_max, exp_min, exp_max
        FROM job_background
        WHERE job_level = ?
    """, (level,))
    bg = cursor.fetchone()

    if bg:
        education, age_min, age_max, exp_min, exp_max = bg
    else:
        education, age_min, age_max, exp_min, exp_max = ("S1", 25, 30, 2, 5)

    cursor.execute("SELECT name, definition, keywords FROM technical_competencies")
    technical = cursor.fetchall()
    cursor.execute("SELECT name, definition, keywords FROM soft_competencies")
    soft = cursor.fetchall()
    conn.close()

    technical_matches = match_competencies(technical, job_description)
    soft_matches = match_competencies(soft, job_description)

    all_comp = technical_matches + soft_matches
    # deduplicate preserving order
    seen = set()
    dedup = []
    for n,d in all_comp:
        if n not in seen:
            dedup.append((n,d))
            seen.add(n)

    # enforce min 5, max 10
    if len(dedup) < 5:
        # pad with soft comps from DB (simple fallback)
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT name, definition FROM soft_competencies")
        extras = cur.fetchall()
        conn.close()
        for n,d in extras:
            if n not in seen:
                dedup.append((n,d))
                seen.add(n)
            if len(dedup) >= 5:
                break

    dedup = dedup[:10]

    return {
        "job_title": job_title,
        "education": education,
        "age_range": f"{age_min}-{age_max} tahun",
        "experience_range": f"{exp_min}-{exp_max} tahun",
        "competencies": [{"name": n, "definition": d} for n,d in dedup],
        "job_level": level
    }

def match_competencies(competency_rows, job_description):
    matches = []
    text = job_description.lower()
    for row in competency_rows:
        name, definition, keywords = row
        for kw in keywords.split(","):
            kw = kw.strip().lower()
            if not kw:
                continue
            # word-boundary search
            if re.search(r'\\b' + re.escape(kw) + r'\\b', text):
                matches.append((name, definition))
                break
    return matches

if __name__ == "__main__":
    # quick local test
    sample = analyze_job_description("Staf Keuangan", "Melaksanakan pelaporan pajak, membuat laporan keuangan dan analisa neraca.")
    import pprint
    pprint.pprint(sample)
