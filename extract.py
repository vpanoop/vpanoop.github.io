import sys
try:
    import Quartz
    from CoreFoundation import NSURL
    from Quartz.PDFKit import PDFDocument
except ImportError:
    print("Quartz/CoreFoundation not available")
    sys.exit(1)

def extract_text(pdf_path):
    url = NSURL.fileURLWithPath_(pdf_path)
    pdf = PDFDocument.alloc().initWithURL_(url)
    if pdf is None:
        print("Could not read PDF")
        return
    
    for i in range(pdf.pageCount()):
        page = pdf.pageAtIndex_(i)
        if page:
            text = page.string()
            if text:
                print(f"--- Page {i+1} ---")
                print(text)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        extract_text(sys.argv[1])
