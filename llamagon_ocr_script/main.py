# This is for the main script, combining the functions/components from other files
from file_handler import convert_to_images
from ocr_parser import detect_text_multiple_images
from cloud_uploader import upload_photo
from paddleocr import PaddleOCR

img_path = "input/Quant Simulation Research.pdf"  # used for debug only, can be deleted later
save_dir = "output/"  # modify if needed

images = convert_to_images(img_path)
ocr_object = PaddleOCR(
    use_angle_cls=True, lang="en"
)  

result = detect_text_multiple_images(
    images, ocr_object, img_path.split("/")[-1].split(".")[0], save_dir
)