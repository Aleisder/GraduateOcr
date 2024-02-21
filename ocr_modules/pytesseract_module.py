from ocr_modules.abstract_ocr_module import AbstractOcrModule
import pytesseract as pyt
from pytesseract import image_to_string
import logging
from config import TESSERACT_PATH, TESSERACT_CONFIG


class PytesseractModule(AbstractOcrModule):
    def __init__(self):
        pyt.pytesseract.tesseract_cmd = TESSERACT_PATH
        self.config = TESSERACT_CONFIG

    def recognize_text(self, image):
        logging.debug('performing recognition in Pytesseract Module')
        return image_to_string(
            image=image,
            lang='jpn',
            config=self.config
        )