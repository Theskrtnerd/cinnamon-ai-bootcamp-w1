# Import necessary modules
import os
from typing import Sequence

import cv2
import docx2pdf
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIF image format opener to handle HEIF files.
# This function needs to be called to enable the application
# to open and process HEIF images.
register_heif_opener()

# List of file types accepted
ACCEPTED_TYPES = [".png", ".tiff", ".pdf", ".docx", ".heic"]


# MUST: Install poppler
def pdf_to_images(pdf_path) -> list:
    images = convert_from_path(pdf_path)
    cv2_images = [cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) for image in images]
    return cv2_images


def convert_to_pdf(doc_path, pdf_path) -> None:
    try:
        # Convert the DOCX file to PDF
        docx2pdf.convert(doc_path, pdf_path)
    except RuntimeError as e:
        print(f"Conversion failed: {e}")


def docx_to_images(docx_path, temp_dir="temp_files") -> list:
    # Convert docx file to pdf file
    os.makedirs(temp_dir, exist_ok=True)
    filename = os.path.splitext(os.path.basename(docx_path))[0]
    pdf_path = os.path.join(temp_dir, filename + ".pdf")
    convert_to_pdf(docx_path, pdf_path)

    # Extract images from .pdf
    images = pdf_to_images(pdf_path)

    # Clean up temporary files
    os.remove(pdf_path)
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)
    return images


def read_image(image_path) -> np.ndarray:
    pil_image = Image.open(image_path)
    pil_image = pil_image.convert("RGB")
    pil_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return pil_image


def convert_to_images(file_path) -> Sequence[np.array]:
    basename = os.path.basename(file_path)
    splited_name = os.path.splitext(basename)
    extension = splited_name[1]
    res = None
    if extension not in ACCEPTED_TYPES:
        raise ValueError("The file type is not supported")
    if extension == ".docx":
        res = docx_to_images(file_path)
    elif extension == ".pdf":
        res = pdf_to_images(file_path)
    else:
        res = [read_image(file_path)]
    return res
