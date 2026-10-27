from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file):
    """Extract text from a PDF uploaded through Streamlit."""
    reader = PdfReader(file)
    pages = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        pages.append(page_text)

    return "\n".join(pages).strip()


def extract_docx_text(file):
    """Extract paragraph text from a DOCX uploaded through Streamlit."""
    document = Document(file)

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs).strip()


def extract_resume_text(file):
    """Detect the uploaded file type and extract its text."""
    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_pdf_text(file)

    if file_name.endswith(".docx"):
        return extract_docx_text(file)

    raise ValueError("Unsupported file type. Please upload PDF or DOCX.")
