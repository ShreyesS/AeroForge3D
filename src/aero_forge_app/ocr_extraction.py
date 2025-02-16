import fitz  # PyMuPDF is great for OCR;  based on Tesseract-OCR
import os
from dotenv import load_dotenv
load_dotenv() # we need to load env vars here

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file"""
    doc = fitz.open(pdf_path)
    extracted_text = [page.get_text("text") for page in doc]
    return "\n".join(extracted_text)

if __name__ == "__main__": # Example Usage:
    pdf_path = "uploads/blueprint_compressor_blade.pdf"
    text = extract_text_from_pdf(pdf_path)
    print(text)
