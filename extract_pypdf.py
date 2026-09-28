import sys
from pypdf import PdfReader

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            print(f"--- Page {i+1} ---")
            print(text)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        extract_text(sys.argv[1])
