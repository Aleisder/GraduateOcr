import base64
import io
from pypdf import PdfReader

from backend.ocr_modules.abstract_ocr_module import AbstractOcrModule


class OcrService:

    def get_reference(self, file: str) -> list[list[str]]:
        decoded: bytes = base64.b64decode(file)
        file_io = io.BytesIO(decoded)
        pdf = PdfReader(file_io)
        document = []
        for page in pdf.pages:
            rows = page.extract_text().split('\n')
            document.append(rows)
        return document

    def get_bordered_image(self, image: bytes) -> bytes:
        return self.experimental_module.mark_symbols_with_borders(image)

    def get_experimental(self, image, lang) -> list[str]:
        return self.experimental_module.recognize_text(image, lang)

    def __init__(self, experimental: AbstractOcrModule):
        self.experimental_module = experimental

    def set_experimental_ocr_module(self, module: AbstractOcrModule):
        self.experimental_module = module
