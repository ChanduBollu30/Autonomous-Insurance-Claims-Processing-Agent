import os

try:
    import pdfplumber
except Exception:
    pdfplumber = None
try:
    import pytesseract
    from pdf2image import convert_from_path
except Exception:
    pytesseract = None
    convert_from_path = None


def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def ocr_pdf(path):
    if convert_from_path is None or pytesseract is None:
        raise RuntimeError("pdf2image and pytesseract are not available for ocr")
    text = ""
    pages = convert_from_path(path)
    for img in pages:
        text += pytesseract.image_to_string(img) + "\n"
    return text


def read_pdf(path):
    text_parts = []
    if pdfplumber is None:
        try:
            return ocr_pdf(path)
        except Exception as e:
            raise RuntimeError("pdfplumber not installed and OCR failed: " + str(e))
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            ptext = page.extract_text()
            if ptext:
                text_parts.append(ptext)
    text = "\n".join(text_parts).strip()
    if not text:
        text = ocr_pdf(path)
    return text


def read_doc(path):
    path = path.lower()
    if path.endswith(".txt"):
        return read_txt(path)
    if path.endswith(".pdf"):
        return read_pdf(path)
    raise ValueError("Unsupported file type: " + path)
