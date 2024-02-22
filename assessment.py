from jiwer import cer, wer
from difflib import context_diff
import difflib


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


def compare_strings(str1, str2):
    # Use difflib to compare the encoded strings
    differ = difflib.Differ()
    diff = differ.compare(str1, str2)
    # Print the differences
    print(type(diff))
    for line in diff:
        print(line)
    # Example usage


string1 = "Hello"
string2 = "Hëpllo"
compare_strings(string1, string2)