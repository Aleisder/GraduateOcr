import os
import pytesseract as pyt
from backend.ocr_modules.abstract_ocr_module import AbstractOcrModule
from dotenv import load_dotenv

# подгружает переменные окружения из файла .env
load_dotenv()


class PytesseractModule(AbstractOcrModule):
    def __init__(self):
        pyt.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')
        self.config = os.getenv('TESSERACT_CONFIG')

    def recognize_text(self, image: bytes, lang: str) -> list[str]:
        return str(
            pyt.image_to_string(
                image=image,
                lang=lang,
                config=self.config
            )
        ).replace(' ', '').split('\n')
