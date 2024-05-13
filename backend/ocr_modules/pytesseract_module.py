import io
import os
import pytesseract as pyt
from pytesseract import Output
from PIL import Image, ImageDraw

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

    def mark_symbols_with_borders(self, image: bytes) -> bytes:
        image_pil = Image.open(io.BytesIO(image))
        draw = ImageDraw.Draw(image_pil)
        data = pyt.image_to_data(image_pil, lang="jpn+chi_sim", output_type=Output.DICT)
        n_boxes = len(data['level'])
        for i in range(n_boxes):
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            conf = float(data['conf'][i])
            text = data['text'][i]
            if conf > 10:
                draw.rectangle(((x - 1, y - 1), (x + w + 1, y + h + 1)), outline='green', width=3)
                draw.text((x, y - 13), text, fill='blue')
        buffer = io.BytesIO()
        # сохранение изображения в буфер
        image_pil.save(buffer, format='PNG')
        return buffer.getvalue()