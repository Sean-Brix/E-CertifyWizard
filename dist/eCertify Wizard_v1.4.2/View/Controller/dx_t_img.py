import sys
from pdf2image import convert_from_path
from View.Controller.gn_crt import generate_one_certificate
from os import getcwd, devnull
from os.path import join, abspath
import logging
import comtypes.client
from comtypes import CoInitialize, CoUninitialize
from docx2pdf import convert as docx2pdf

poppler_path = join(getcwd(), 'poppler_bin', 'Release', 'poppler', 'Library', 'bin')

def convert_docx_to_pdf(input_path, output_path):
    try:
        CoInitialize()
        # Try using COM automation first (MS Word)
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = False
        try:
            doc = word.Documents.Open(abspath(input_path))
            doc.SaveAs(abspath(output_path), FileFormat=17)  # 17 = PDF format
            doc.Close()
            return True
        finally:
            word.Quit()
            CoUninitialize()
    except Exception as e:
        logging.debug(f"COM automation failed, falling back to docx2pdf: {e}")
        # Fall back to docx2pdf if COM fails
        try:
            with open(devnull, 'w') as f:
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = f
                sys.stderr = f
                docx2pdf(input_path)
                sys.stdout = old_stdout
                sys.stderr = old_stderr
            return True
        except Exception as e:
            logging.error(f"All conversion methods failed: {e}")
            raise

def convert_dtimg(file_path):
    try:
        image_path = None

        # Convert DOCX to PDF
        pdf_path = file_path.replace('.docx', '.pdf')
        convert_docx_to_pdf(file_path, pdf_path)
    
        # Convert PDF to PNG
        image_path = pdf_path.replace('.pdf', '.png')
        pdf_to_image(pdf_path, image_path)

    except Exception as e: 
        logging.error(f"Error processing file: {e}", exc_info=True)
        return

    return image_path

def convert_one_img(name, input_filename, keyValue_pairs = [['[name]', '[honor]', '[quarter]']]):
    try:
        image_path = None
        generate_one_certificate(name, input_filename, keyValue_pairs)
        file_path = join(getcwd(), 'temporary', 'preview_img.docx')
    
        # Convert DOCX to PDF
        pdf_path = file_path.replace('.docx', '.pdf')
        convert_docx_to_pdf(file_path, pdf_path)

        # Convert PDF to PNG
        image_path = pdf_path.replace('.pdf', '.png')
        pdf_to_image(pdf_path, image_path)

    except Exception as e: 
        logging.error(f"Error processing file: {e}", exc_info=True)
        return None

    return image_path

def pdf_to_image(pdf_path, image_path):
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    images[0].save(image_path, 'PNG')


