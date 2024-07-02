import json
import os

import cv2
import numpy as np
from paddleocr import PaddleOCR

ocr_object = PaddleOCR(
    use_angle_cls=True, lang="en"
)  # supported languages: `ch`, `en`, `fr`, `german`, `korean`, `japan`
img_path = "resource/images/champ.jpg"  # used for debug only, can be deleted later
save_dir = "resource/output"  # modify if needed


def box_as_percent(box: list, img_width: int, img_height: int) -> list:
    x1, y1 = box[0]
    x2, y2 = box[2]
    x1_percent = round(x1 / img_width, 4)
    y1_percent = round(y1 / img_height, 4)
    x2_percent = round(x2 / img_width, 4)
    y2_percent = round(y2 / img_height, 4)
    return [x1_percent, y1_percent, x2_percent, y2_percent]


def detect_text_single_image(image: np.ndarray, ocr_object) -> dict:
    json_output = []
    result = ocr_object.ocr(image, cls=True)
    for line in result:
        line_instance = {}
        line_instance["box"] = box_as_percent(line[0], image.shape[1], image.shape[0])
        line_instance["text"] = line[1][0]
        line_instance["score"] = line[1][1]
        json_output.append(line_instance)
    return json_output


def save_json_file(json_output: dict, file_name: str, output_folder: str) -> None:
    json_file = os.path.join(output_folder, file_name + ".json")
    with open(json_file, "w") as f:
        json.dump(json_output, f)


def save_visualized_image(
    image: np.ndarray, image_id: int, ocr_result: list, output_folder: str
) -> None:
    img_width = image.shape[1]
    img_height = image.shape[0]
    for line in ocr_result:
        box = line["box"]
        x1 = int(box[0] * img_width)
        y1 = int(box[1] * img_height)
        x2 = int(box[2] * img_width)
        y2 = int(box[3] * img_height)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.imwrite(os.path.join(output_folder, f"{image_id}.jpg"), image)


def detect_text_multiple_images(
    images: list[np.ndarray], ocr_object, file_name: str, save_dir: str
) -> None:
    # prepare output folder to save images and json file
    json_output = {}
    output_folder = os.path.join(save_dir, file_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # process each image and save the result
    for image_id, image in enumerate(images):
        ocr_result = detect_text_single_image(image, ocr_object)
        json_output[image_id] = ocr_result
        save_visualized_image(image, image_id, ocr_result, output_folder)
    save_json_file(json_output, file_name, output_folder)


# if "__name__" == "__main__":
#    images = [read_image(img_path)]
#    result = detect_text_multiple_images(
#        images, ocr_object, img_path.split("/")[-1].split(".")[0], save_dir
#    )

# for idx in range(len(result)):
#     line = result[idx]
#     print(f"Box: {line[0]}")
#     print(f"Text: {line[1][0]}")
#     print(f"Score: {line[1][1]}")
#     print()

# # # draw result
# image = Image.open(img_path).convert('RGB')

# output_img_path = img_path.split('.')[0] + '_result.jpg'
# im_show = draw_ocr(image, boxes, texts, scores, font_path='resource/fonts/simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save(output_img_path)
