from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(results, avg_score, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"Average Score: {avg_score}%", styles["Title"]))

    for r in results:
        content.append(Paragraph(f"Q: {r['question']}", styles["Normal"]))
        content.append(Paragraph(f"A: {r['answer']}", styles["Normal"]))
        content.append(Paragraph(f"Score: {r['score']}%", styles["Normal"]))
        content.append(Paragraph(" ", styles["Normal"]))

    doc.build(content)