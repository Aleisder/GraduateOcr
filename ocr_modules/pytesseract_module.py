from ocr_modules.abstract_ocr_module import AbstractOcrModule
import pytesseract as pyt
from pytesseract import image_to_string
import logging


class PytesseractModule(AbstractOcrModule):
    def __init__(self):
        pyt.pytesseract.tesseract_cmd = r'A:\Devs\Modules\tesseract\tesseract.exe'
        self.config = r'--tessdata-dir "A:\Devs\Modules\tesseract\tessdata"'

    def recognize_text(self, image):
        logging.debug('performing recognition in Pytesseract Module')
        return image_to_string(
            image=image,
            config=self.config
        )