import pytesseract as pyt
from pytesseract import image_to_string

from frontend.config import TESSERACT_PATH, TESSERACT_CONFIG
from frontend.ocr_modules.abstract_ocr_module import AbstractOcrModule


class PytesseractModule(AbstractOcrModule):
    def __init__(self):
        pyt.pytesseract.tesseract_cmd = TESSERACT_PATH
        self.config = TESSERACT_CONFIG

    def recognize_text(self, image, lang) -> list[str]:
        return str(
            image_to_string(
                image=image,
                lang=lang,
                config=self.config
            )
        ).replace(' ', '').split('\n')
