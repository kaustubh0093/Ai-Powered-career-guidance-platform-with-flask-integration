import os
import io
import PyPDF2
import docx

def extract_text_from_file(file):
    filename = file.filename.lower()
    content = ""
    
    if filename.endswith('.txt'):
        content = file.read().decode('utf-8')
    
    elif filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        for page in pdf_reader.pages:
            content += page.extract_text() + "\n"
    
    elif filename.endswith('.docx') or filename.endswith('.doc'):
        doc = docx.Document(io.BytesIO(file.read()))
        content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    return content.strip()
