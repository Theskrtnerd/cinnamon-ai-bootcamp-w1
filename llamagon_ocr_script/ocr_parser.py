from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

# img_path = "resource/images/lm5.jpg"
img_path = "resource/images/bracelets.png"

ocr = PaddleOCR(
    use_angle_cls=True, lang="en"
)  # supported languages: "ch", "en", "fr", "german", "korean", "japan"
result = ocr.ocr(img_path, cls=True)

for idx in range(len(result)):
    line = result[idx]
    print(f"Box: {line[0]}")
    print(f"Text: {line[1][0]}")
    print(f"Score: {line[1][1]}")
    print()

# # draw result
image = Image.open(img_path).convert("RGB")
boxes = [line[0] for line in result]
texts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
output_img_path = img_path.split(".")[0] + "_result.jpg"
im_show = draw_ocr(image, boxes, texts, scores, font_path="resource/fonts/simfang.ttf")
im_show = Image.fromarray(im_show)
im_show.save(output_img_path)
