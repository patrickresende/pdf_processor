import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import logging
from rapidfuzz import process, fuzz
from employee import employee_names  # Importa a lista de nomes dos funcionários


# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# Utility functions
def ensure_directory_exists(directory):
    """Ensures the given directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def extract_text_from_page(page):
    """Extract text from a PDF page."""
    return page.get_text("text")


def extract_text_with_ocr(page):
    """Extract text using OCR if the page text is empty."""
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return pytesseract.image_to_string(img)


def identify_employee_name(text, employee_list, threshold=90):
    """Identifica o nome do funcionário usando correspondência fuzzy."""
    matches = process.extract(text, employee_list, scorer=fuzz.partial_ratio)
    for match, score, _ in matches:
        if score >= threshold:
            return match
    return "NOME NÃO ENCONTRADO"


def log_unmatched_name(page_number, text, output_file="unmatched_names.txt"):
    """Registra o nome não identificado e a página."""
    with open(output_file, "a", encoding="utf-8") as log_file:
        log_file.write(f"Página {page_number}: {text}\n")


def process_pdf(pdf_file_path, output_dir, year, month, progress_callback=None, cancel_callback=None):
    """
    Processes the PDF and organizes pages by employee.
    
    Parameters:
        pdf_file_path (str): Path to the input PDF.
        output_dir (str): Directory to save processed PDFs.
        year (str): Year for the output files.
        month (str): Month for the output files.
        progress_callback (function): Function to update progress in the UI.
        cancel_callback (function): Function to check if the process is canceled.
    """
    try:
        doc = fitz.open(pdf_file_path)
        ensure_directory_exists(output_dir)

        for i, page in enumerate(doc):
            if cancel_callback and cancel_callback():
                logging.info("Process canceled by user.")
                return

            # Extract text
            text = extract_text_from_page(page).strip()
            if not text:
                text = extract_text_with_ocr(page)

            # Log text for debugging
            logging.info(f"Texto extraído da página {i + 1}: {text}")

            # Identify employee
            employee_name = identify_employee_name(text, employee_names)

            if employee_name == "NOME NÃO ENCONTRADO":
                log_unmatched_name(i + 1, text)
                logging.warning(f"Nome não encontrado na página {i + 1}")
                continue

            # Create directory for employee
            employee_folder = os.path.join(output_dir, employee_name)
            ensure_directory_exists(employee_folder)

            # Save individual PDF
            pdf_filename = f"{employee_name} - Recibo - {month}-{year}.pdf"
            output_pdf_path = os.path.join(employee_folder, pdf_filename)

            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=i, to_page=i)
            new_doc.save(output_pdf_path)
            new_doc.close()

            logging.info("Arquivo salvo: %s", output_pdf_path)

            # Update progress bar (if callback provided)
            if progress_callback:
                progress_callback(i + 1, len(doc))

        logging.info("PDF processing completed successfully.")
    except Exception as e:
        logging.error(f"Erro ao processar o PDF: {e}")
        raise
