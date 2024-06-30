import cv2
from pdf2image import convert_from_path
from PIL import Image
from pillow_heif import register_heif_opener
import os
import subprocess
import numpy as np
from typing import Sequence


register_heif_opener()
LIBREOFFICE_PATH = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
ACCEPT_TYPES = ['.png', '.tiff', '.pdf', '.doc', '.docx', '.heic']


# MUST: Install poppler
def pdf_to_images(pdf_path) -> list:
    images = convert_from_path(pdf_path)
    cv2_images = [cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                  for image in images]
    return cv2_images


# MUST: Install libreoffice
def convert_to_pdf(doc_path, temp_dir) -> None:
    try:
        subprocess.run([LIBREOFFICE_PATH, '--headless', '--convert-to', 'pdf',
                        '--outdir', temp_dir, doc_path],
                       check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def doc_to_images(doc_path, temp_dir='temp_files') -> list:
    os.makedirs(temp_dir, exist_ok=True)
    # Convert .doc to .pdf
    convert_to_pdf(doc_path, temp_dir)
    filename = os.path.splitext(os.path.basename(doc_path))[0]
    pdf_path = os.path.join(temp_dir, filename+".pdf")

    # Extract images from .pdf
    images = pdf_to_images(pdf_path)

    # Clean up temporary files
    os.remove(pdf_path)
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)
    return images


def read_image(image_path) -> np.array:
    pil_image = Image.open(image_path)
    pil_image = pil_image.convert('RGB')
    return np.asarray(pil_image)


def convert_to_images(file_path) -> Sequence[np.array]:
    basename = os.path.basename(file_path)
    splited_name = os.path.splitext(basename)
    extension = splited_name[1]
    res = None
    if extension not in ACCEPT_TYPES:
        raise ValueError("The file type is not supported")
    if extension in [".doc", ".docx"]:
        res = doc_to_images(file_path)
    elif extension == ".pdf":
        res = pdf_to_images(file_path)
    else:
        res = [read_image(file_path)]
    return res
