from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime

def export_analysis_to_pdf(filename, job_title, job_desc, education, age_range, exp_range, job_level, competencies):
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=40,leftMargin=40, topMargin=40,bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []
    now = datetime.datetime.now().strftime("%d %b %Y %H:%M")
    story.append(Paragraph("Job Analysis Report", styles['Title']))
    story.append(Paragraph(f"Generated: {now}", styles['Normal']))
    story.append(Spacer(1,12))
    story.append(Paragraph(f"<b>Nama Jabatan:</b> {job_title}", styles['Normal']))
    story.append(Paragraph(f"<b>Level Jabatan:</b> {job_level}", styles['Normal']))
    story.append(Spacer(1,8))
    story.append(Paragraph("<b>Uraian Jabatan:</b>", styles['Normal']))
    story.append(Paragraph(job_desc.replace("\\n","<br/>"), styles['Normal']))
    story.append(Spacer(1,12))
    story.append(Paragraph(f"<b>Pendidikan:</b> {education}", styles['Normal']))
    story.append(Paragraph(f"<b>Usia:</b> {age_range}", styles['Normal']))
    story.append(Paragraph(f"<b>Pengalaman:</b> {exp_range}", styles['Normal']))
    story.append(Spacer(1,12))
    story.append(Paragraph("<b>Standar Kompetensi:</b>", styles['Heading2']))
    for i, comp in enumerate(competencies, 1):
        story.append(Paragraph(f"{i}. <b>{comp.get('name')}</b>", styles['Normal']))
        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;{comp.get('definition')}", styles['Normal']))
        story.append(Spacer(1,6))
    doc.build(story)

if __name__ == "__main__":
    print("pdf_detector module")
