



# sua ham read_image de giong voi pdf->img, doc->img va tuong thich voi ocr_parser
def read_image(image_path) -> np.ndarray:
    pil_image = Image.open(image_path)
    pil_image = pil_image.convert('RGB')
    pil_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return pil_image