from easyocr import Reader
from ocr_modules.abstract_ocr_module import AbstractOcrModule
import logging
import io


class EasyOcrModule(AbstractOcrModule):

    def __init__(self):
        self.reader = Reader(lang_list=['ru'])

    def recognize_text(self, image):
        print("EasyOCR is translating...")
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        image_bytes = img_byte_arr.getvalue()
        result = self.reader.readtext(image_bytes)
        text = ''
        for block in result:
            text += block[1] + ' '
        return text.replace('  ', ' ')
