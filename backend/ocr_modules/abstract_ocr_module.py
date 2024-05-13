from abc import ABC, abstractmethod


class AbstractOcrModule(ABC):
    @abstractmethod
    def recognize_text(self, image, lang) -> list[str]:
        pass

    @abstractmethod
    def mark_symbols_with_borders(self, image: bytes) -> bytes:
        pass
