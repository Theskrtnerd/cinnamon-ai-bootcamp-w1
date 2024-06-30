import numpy as np
import pytest
import os
from llamagon_ocr_script.file_handler import (
    convert_to_images,
    doc_to_images,
    pdf_to_images,
    read_image,
)


TEST_FOLDER = "tests/test_files"


def test_pdf_file():
    pdf_path = os.path.join(TEST_FOLDER, "test.pdf")
    assert type(pdf_to_images(pdf_path)) == list


def test_doc_file():
    file_path = os.path.join(TEST_FOLDER, "test.doc")
    assert type(doc_to_images(file_path)) == list


def test_tiff_file():
    tiff_path = os.path.join(TEST_FOLDER, "test.tiff")
    assert type(read_image(tiff_path)) == np.ndarray


def test_png_file():
    png_path = os.path.join(TEST_FOLDER, "test.png")
    assert type(read_image(png_path)) == np.ndarray


def test_heic_file():
    heic_path = os.path.join(TEST_FOLDER, "test.heic")
    assert type(read_image(heic_path)) == np.ndarray


def test_other_file():
    file_path = os.path.join(TEST_FOLDER, "test.txt")
    with pytest.raises(ValueError) as e:
        convert_to_images(file_path)
    assert str(e.value) == "The file type is not supported"
