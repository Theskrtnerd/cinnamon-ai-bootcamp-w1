import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from llamagon_ocr_script.ocr_parser import (
    detect_text_multiple_images,
    detect_text_single_image,
    save_image,
    save_json_file,
    save_visualized_image,
)

sys.path.append("../llamagon_ocr_script")


class TestOCRParser(unittest.TestCase):
    @patch(
        "ocr_parser.PaddleOCR"
    )  # mock_paddleocr serves as a mock instance of any PaddleOCR object
    def test_detect_text_single_image(self, mock_paddleocr):
        # Mock the OCR result.
        mock_ocr_result = [[[[10, 20], [10, 30], [50, 30], [50, 20]], ["text", 0.99]]]
        mock_ocr_instance = mock_paddleocr.return_value
        mock_ocr_instance.ocr.return_value = mock_ocr_result

        # Create a dummy image
        image = np.zeros((100, 100, 3), dtype=np.uint8)

        # Call the function
        result = detect_text_single_image(image, mock_ocr_instance)

        # Expected result
        expected_result = [{"box": [10, 20, 50, 30], "text": "text", "score": 0.99}]

        # Assertions
        self.assertEqual(
            result, expected_result
        )  # Check that function returns expected result
        mock_ocr_instance.ocr.assert_called_once_with(
            image, cls=True
        )  # Check that 'ocr' method was called exactly once with listed arguments

    @patch(
        "ocr_parser.os.path.join", return_value="dummy_path.json"
    )  # Mock any join method with specified return value
    @patch("ocr_parser.open", new_callable=unittest.mock.mock_open)
    def test_save_json_file(self, mock_open, mock_path_join):
        json_output = {"dummy_key": "dummy_value"}
        file_name = "dummy_file"
        output_folder = "dummy_folder"

        save_json_file(json_output, file_name, output_folder)

        # Assertions
        mock_path_join.assert_called_once_with(output_folder, file_name + ".json")
        self.assertEqual(
            mock_path_join(output_folder, file_name + ".json"), "dummy_path.json"
        )
        mock_open.assert_called_once_with(
            os.path.join(output_folder, file_name + ".json"), "w"
        )

    @patch("ocr_parser.cv2.imwrite")
    @patch("ocr_parser.os.path.join", return_value="dummy_path.jpg")
    def test_save_image(self, mock_path_join, mock_imwrite):
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        image_id = 1
        output_folder = "dummy_folder"

        save_image(image, image_id, output_folder)

        # Assertions
        mock_path_join.assert_called_once_with(output_folder, "1.jpg")
        self.assertEqual(mock_path_join(output_folder, "1.jpg"), "dummy_path.jpg")
        mock_imwrite.assert_called_once_with("dummy_path.jpg", image)

    @patch("ocr_parser.cv2.imwrite")
    @patch("ocr_parser.os.path.join", return_value="dummy_path.jpg")
    def test_save_visualized_image(self, mock_path_join, mock_imwrite):
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        image_id = 1
        output_folder = "dummy_folder"
        ocr_result = [{"box": [10, 20, 50, 30], "text": "text", "score": 0.99}]

        save_visualized_image(image, image_id, output_folder, ocr_result)

        # Assertions
        mock_path_join.assert_called_once_with(output_folder, "visualized_1.jpg")
        self.assertEqual(
            mock_path_join(output_folder, "visualized_1.jpg"), "dummy_path.jpg"
        )
        mock_imwrite.assert_called_once_with("dummy_path.jpg", image)

    @patch("ocr_parser.detect_text_single_image")
    @patch("ocr_parser.save_image")
    @patch("ocr_parser.save_visualized_image")
    @patch("ocr_parser.save_json_file")
    @patch("ocr_parser.os.makedirs")
    @patch("ocr_parser.os.path.exists", return_value=False)
    def test_detect_text_multiple_images(
        self,
        mock_path_exists,
        mock_makedirs,
        mock_save_json_file,
        mock_save_visualized_image,
        mock_save_image,
        mock_detect_text_single_image,
    ):
        # Create a dummy list of images
        images = [np.zeros((100, 100, 3), dtype=np.uint8) for _ in range(3)]
        ocr_object = MagicMock()
        file_name = "test"
        save_dir = "test_files"

        mock_detect_text_single_image.return_value = [
            {"box": [10, 20, 50, 30], "text": "text", "score": 0.99}
        ]

        detect_text_multiple_images(
            images, ocr_object, file_name, save_dir, save_visualized=True
        )

        # Assertions
        output_folder = os.path.join(save_dir, file_name)
        mock_path_exists.assert_called_once_with(output_folder)
        mock_makedirs.assert_called_once_with(output_folder)


if __name__ == "__main__":
    unittest.main()
