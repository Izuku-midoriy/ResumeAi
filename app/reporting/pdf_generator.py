import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class PDFGenerator:
    """Generates a professional PDF report containing the ATS score and job matches."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = self.styles['Title']
        self.heading_style = self.styles['Heading2']
        self.normal_style = self.styles['Normal']
        
        # Custom styles
        self.match_style = ParagraphStyle(
            'MatchStyle', 
            parent=self.styles['Normal'],
            textColor=colors.green,
            fontName='Helvetica-Bold'
        )
        self.no_match_style = ParagraphStyle(
            'NoMatchStyle', 
            parent=self.styles['Normal'],
            textColor=colors.red,
            fontName='Helvetica-Bold'
        )

    def generate_report(self, information, score, ranked_jobs):
        """
        Creates the PDF report in memory.
        Returns the raw PDF bytes.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        elements = []
        
        # 1. Title
        elements.append(Paragraph("AI Resume Intelligence Report", self.title_style))
        elements.append(Spacer(1, 12))
        
        # 2. Candidate Info
        elements.append(Paragraph("Candidate Information", self.heading_style))
        
        email = information.get('email') or "Not found"
        phone = information.get('phone') or "Not found"
        elements.append(Paragraph(f"<b>Email:</b> {email}", self.normal_style))
        elements.append(Paragraph(f"<b>Phone:</b> {phone}", self.normal_style))
        elements.append(Spacer(1, 12))
        
        # 3. ATS Score
        elements.append(Paragraph("ATS Analysis", self.heading_style))
        elements.append(Paragraph(f"<b>Overall Resume Score:</b> {score} / 100", self.normal_style))
        elements.append(Spacer(1, 12))
        
        # 4. Top Job Matches
        elements.append(Paragraph("Top Recommended Jobs", self.heading_style))
        elements.append(Spacer(1, 6))
        
        for i, job in enumerate(ranked_jobs[:10]):
            # Job Title and Company
            title = job.get('title', job.get('job_title', 'Unknown Title'))
            company = job.get('company', 'Unknown Company')
            location = job.get('location', 'Remote')
            
            elements.append(Paragraph(f"<b>{i+1}. {title}</b> — {company}", self.normal_style))
            elements.append(Paragraph(f"Location: {location}", self.normal_style))
            
            # AI Prediction (new multi-class format)
            prediction = job.get("ml_prediction", "Unknown")
            ranking_score = round(job.get("ranking_score", 0.0) * 100, 1)
            probs = job.get("ml_probabilities", {})
            p_good = round(probs.get("Good Fit", 0) * 100, 1)
            p_potential = round(probs.get("Potential Fit", 0) * 100, 1)
            p_no = round(probs.get("No Fit", 0) * 100, 1)
            
            if prediction == "Good Fit":
                pred_para = Paragraph(f"AI Verdict: GOOD FIT (Ranking Score: {ranking_score}%)", self.match_style)
            elif prediction == "Potential Fit":
                pred_para = Paragraph(f"AI Verdict: POTENTIAL FIT (Ranking Score: {ranking_score}%)", self.normal_style)
            else:
                pred_para = Paragraph(f"AI Verdict: NO FIT (Ranking Score: {ranking_score}%)", self.no_match_style)
            elements.append(pred_para)
            
            # Class Probabilities
            elements.append(Paragraph(
                f"Probabilities — Good Fit: {p_good}% | Potential Fit: {p_potential}% | No Fit: {p_no}%",
                self.normal_style
            ))
            
            # AI Explanation
            explanation = job.get("explanation", "Explanation not available.")
            elements.append(Paragraph(f"Explanation: {explanation}", self.normal_style))
            
            elements.append(Spacer(1, 12))
            
        # Build the PDF
        doc.build(elements)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
