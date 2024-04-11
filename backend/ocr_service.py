import base64
import io
from abc import ABC, abstractmethod
from pypdf import PdfReader


class OcrModule(ABC):
    @abstractmethod
    def recognize_text(self, image, lang) -> list[str]:
        pass


class OcrServiceAbstract(ABC):

    @abstractmethod
    def get_reference(self, file: str):
        pass

    @abstractmethod
    def get_experimental(self, file):
        pass

    @abstractmethod
    def set_experimental_ocr_module(self, module: OcrModule):
        pass


class OcrService(OcrServiceAbstract):

    def get_reference(self, file: str) -> list[list[str]]:
        decoded: bytes = base64.b64decode(file)
        file_io = io.BytesIO(decoded)
        pdf = PdfReader(file_io)
        document = []
        for page in pdf.pages:
            rows = page.extract_text().split('\n')
            document.append(rows)
        return document

    def get_experimental(self, file) -> list[str]:
        return self.experimental_module.recognize_text(file, 'jpn')

    def __init__(self, experimental: OcrModule):
        self.experimental_module = experimental

    def get_recognitions(self, image, lang) -> tuple[list[str], list[str]]:

        experimental = self.experimental_module.recognize_text(image, lang)
        return ['test'], experimental

    def set_experimental_ocr_module(self, module: OcrModule):
        self.experimental_module = module
