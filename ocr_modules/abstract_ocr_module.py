from abc import ABC, abstractmethod


class AbstractOcrModule(ABC):
    @abstractmethod
    def recognize_text(self, image: bytes):
        pass
