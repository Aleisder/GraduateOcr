from jiwer import cer, wer
from difflib import context_diff


def get_page_analytics(reference: str, hypothesis: str):
    return wer(reference, hypothesis), cer(reference, hypothesis)

#
# reference = 'User is making somee shit'
# hypo = 'User i makin somet shit'
#
# wer = wer(reference, hypo)
# cer = cer(reference, hypo, return_dict=True)
#
# print(wer)
# print(cer)