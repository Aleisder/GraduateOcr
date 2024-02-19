from jiwer import cer, wer


def get_page_analytics(reference: str, hypothesis: str):
    return wer(reference, hypothesis), cer(reference, hypothesis)
