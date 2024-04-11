
class OcrDocument:

    def __init__(self, reference: list[list[str]], experimental: list[list[str]]):
        self.reference: list[list[str]] = reference
        self.experimental: list[list[str]] = experimental

    def to_plain_text(self) -> tuple[str, str]:
        ref = ''
        for page in self.reference:
            for line in page:
                ref += line + '\n'
        exp = ''
        for page in self.experimental:
            for line in page:
                exp += line + '\n'
        return ref, exp
