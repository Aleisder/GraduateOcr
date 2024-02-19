from abc import ABC, abstractmethod


class OcrModule(ABC):
    @abstractmethod
    def recognize_text(self, image):
        pass


class OcrServiceAbstract(ABC):

    @abstractmethod
    def get_recognitions(self, image):
        pass

    @abstractmethod
    def set_reference_ocr_module(self, module: OcrModule):
        pass

    @abstractmethod
    def set_experimental_ocr_module(self, module: OcrModule):
        pass


class OcrService(OcrServiceAbstract):
    def __init__(self, reference: OcrModule, experimental: OcrModule):
        self.reference_module = reference
        self.experimental_module = experimental

    def get_recognitions(self, image):
        reference = self.reference_module.recognize_text(image)
        experimental = self.experimental_module.recognize_text(image)
        return reference, experimental

    def set_reference_ocr_module(self, module: OcrModule):
        self.reference_module = module

    def set_experimental_ocr_module(self, module: OcrModule):
        self.experimental_module = module
