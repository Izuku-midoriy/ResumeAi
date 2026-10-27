from reportlab.pdfgen import canvas

pdf_path = "C:\\Users\\kunal\\OneDrive - Vidyalankar Institute of Technology\\Desktop\\AML\\dummy_resume.pdf"
c = canvas.Canvas(pdf_path)
c.drawString(100, 750, "John Doe")
c.drawString(100, 730, "Email: john.doe@example.com")
c.drawString(100, 710, "Skills: Python, Django, AWS, React, Machine Learning, PostgreSQL")
c.drawString(100, 690, "Experience: 5 years software engineer building scalable backend systems.")
c.drawString(100, 670, "Education: Bachelor of Science in Computer Science.")
c.save()
print(f"Created {pdf_path}")
