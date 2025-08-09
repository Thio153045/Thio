import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

DB_PATH = "data/competencies.db"

def export_database_to_pdf(filename, comp_type="technical"):
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=40,leftMargin=40, topMargin=40,bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []

    title = "Technical Competencies" if comp_type=="technical" else "Soft Competencies"
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1,12))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if comp_type == "technical":
        cur.execute("SELECT name, definition, keywords FROM technical_competencies")
    else:
        cur.execute("SELECT name, definition, keywords FROM soft_competencies")
    rows = cur.fetchall()
    conn.close()

    for i, (name, definition, keywords) in enumerate(rows, 1):
        story.append(Paragraph(f"{i}. <b>{name}</b>", styles['Normal']))
        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;{definition}", styles['Normal']))
        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;<i>Keywords:</i> {keywords}", styles['Normal']))
        story.append(Spacer(1,6))

    doc.build(story)

if __name__ == "__main__":
    export_database_to_pdf("competencies_export.pdf", "technical")
    print("Exported to competencies_export.pdf")
