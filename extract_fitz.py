import sys
import fitz

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        page = doc[i]
        text = page.get_text()
        print(f"--- Page {i+1} ---")
        print(text)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        extract_text(sys.argv[1])
