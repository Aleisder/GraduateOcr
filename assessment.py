from jiwer import cer, wer


def get_page_analytics(reference: str, hypothesis: str):
    return wer(reference, hypothesis), cer(reference, hypothesis)


reference = '細かい部分を描く前に必要な全ての図が描けるようにまず全体の配置を決定する'
hypo = '細かい部分を描く前に 必要な全ての図が描けるように ますず全体の配置を決定する'


wer = wer(reference, hypo)
cer = cer(reference, hypo, return_dict=True)

print(wer)
print(cer)
