import argparse

from cloud_uploader import upload_folder
from file_handler import convert_to_images
from ocr_parser import detect_text_multiple_images
from paddleocr import PaddleOCR


def main(file_name, upload, input_folder, output_folder):
    img_path = f"{input_folder}/{file_name}"
    save_dir = output_folder  # Use the provided output folder

    images = convert_to_images(img_path)
    ocr_object = PaddleOCR(use_angle_cls=True, lang="en")

    folder_name = file_name.split(".")[0]

    detect_text_multiple_images(images, ocr_object, folder_name, save_dir)

    if upload:
        upload_folder(folder_name, save_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process a PDF file and optionally upload the result to the cloud."
    )
    parser.add_argument(
        "file_name", type=str, help="The name of the PDF file to process."
    )
    parser.add_argument(
        "--upload", action="store_true", help="Upload the result folder to the cloud."
    )
    parser.add_argument(
        "--input_folder",
        type=str,
        default="input",
        help="The input folder containing the PDF file.",
    )
    parser.add_argument(
        "--output_folder",
        type=str,
        default="output",
        help="The folder to save the output images and text.",
    )

    args = parser.parse_args()

    main(args.file_name, args.upload, args.input_folder, args.output_folder)
