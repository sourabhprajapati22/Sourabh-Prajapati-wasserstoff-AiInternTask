import fitz  # PyMuPDF
import pdfplumber
from paddleocr import PaddleOCR
import cv2
import numpy as np
from io import BytesIO
from pathlib import Path

ocr = PaddleOCR(use_angle_cls=True, lang='en')  # OCR engine

def is_scanned_pdf(page):
    """Heuristic: If there's no text on a page, assume it's scanned/image-based."""
    return not page.get_text("text").strip()


def extract_text_fitz(page):
    text_pages = []
    text_pages.append(page.get_text())
    return text_pages


def extract_tables_pagewise(pdf_path,i):
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        page=pdf.pages[i]
        page_tables = page.extract_tables()
        for tbl in page_tables:
            all_tables.append(tbl)

    return all_tables


def extract_text_ocr(page):
    extracted_text = []
    pix = page.get_pixmap(dpi=300)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:  # RGBA
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    result = ocr.ocr(img)[0]
    text = "\n".join([line[1][0] for line in result])
    extracted_text.append(text)
    return extracted_text



def extract_from_pdf(pdf_path):
    pdf_path = Path(pdf_path)
    doc = fitz.open(pdf_path)

    output_text={}

    for i,page in enumerate(doc):
        print(i)
        if is_scanned_pdf(page):
            output_text.update({
                i+1:{
                "method": "ocr",
                "text": extract_text_ocr(page),
                "tables": []
                }
            })
        else:
            output_text.update({
                i+1:{
                "method": "text+table",
                "text": extract_text_fitz(page),
                "tables": extract_tables_pagewise(pdf_path,i)
                }
            })
    
    final_output={}
    for page_num, data in output_text.items():
        combined_output=""
        # combined_output += f"\n Page {page_num+1}:\n"

        if data['text']:
            combined_output += data['text'][0] + "\n"

        if data['tables']:
            for table_index, table in enumerate(data['tables']):
                combined_output += f"\n Table {table_index + 1}:\n"
                table_string = "\n".join(["\t".join([str(cell) if cell is not None else "" for cell in row]) for row in table])
                # table_string = "\n".join(["\t".join(row) for row in table])
                combined_output += table_string + "\n"
        final_output.update({page_num:combined_output})


    return final_output


# if __name__ == "__main__":
#     result = extract_from_pdf("backend/data/EJ1172284.pdf")
#     print(result)