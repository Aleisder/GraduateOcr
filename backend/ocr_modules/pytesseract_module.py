import pytesseract as pyt

from backend.config import TESSERACT_PATH, TESSERACT_CONFIG
from backend.ocr_modules.abstract_ocr_module import AbstractOcrModule


class PytesseractModule(AbstractOcrModule):
    def __init__(self):
        pyt.pytesseract.tesseract_cmd = TESSERACT_PATH
        self.config = TESSERACT_CONFIG

    def recognize_text(self, image, lang) -> list[str]:
        return str(
            pyt.image_to_string(
                image=image,
                lang=lang,
                config=self.config
            )
        ).replace(' ', '').split('\n')
