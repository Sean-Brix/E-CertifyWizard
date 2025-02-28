import sys
from docx2pdf import convert
from pdf2image import convert_from_path
from View.Controller.gn_crt import generate_one_certificate
from os import devnull, getcwd
from os.path import join
import logging

poppler_path = join(getcwd(), 'poppler_bin', 'Release', 'poppler', 'Library', 'bin')

def convert_dtimg(file_path):

    try:
        image_path = None

        with open(devnull, 'w') as f:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = f
            sys.stderr = f

            convert(file_path)
        
            pdf_path = file_path.replace('.docx', '.pdf')
            images = convert_from_path(pdf_path, poppler_path=poppler_path)

            sys.stdout = old_stdout
            sys.stderr = old_stderr

            image_path = file_path.replace('.docx', '.png')
            images[0].save(image_path, 'PNG')

    except Exception as e: 
        logging.error(f"\n\n\n\nError processing file: {e}\n\n\n\n", exc_info=True)
        return

    return image_path

def convert_one_img(name, input_filename, keyValue_pairs = [['[name]', '[honor]', '[quarter]']]):
    try:
        image_path = None
        generate_one_certificate(name, input_filename, keyValue_pairs)
        file_path = join(getcwd(), 'temporary', 'preview_img.docx')

        with open(devnull, 'w') as f:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = f
            sys.stderr = f
    
            convert(file_path)
            pdf_path = file_path.replace('.docx', '.pdf')
            images = convert_from_path(pdf_path, poppler_path=poppler_path)

            sys.stdout = old_stdout
            sys.stderr = old_stderr

            image_path = file_path.replace('.docx', '.png')
            images[0].save(image_path, 'PNG')

    except Exception as e: 
        logging.error(f"\n\n\n\nError processing file: {e}\n\n\n\n", exc_info=True)
        return

    return image_path
        

    