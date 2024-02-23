from difflib import Differ
from dash.html import Span


def build_from_differ_compare(reference: str, hypothesis: str) -> list[Span]:
    differ = Differ()
    diff = differ.compare(reference, hypothesis)
    children = []
    for symbol in diff:
        if symbol[0] == '+':
            class_name = 'wrong-symbol'
        elif symbol[0] == '-':
            class_name = 'missed-symbol'
        else:
            class_name = 'correct-symbol'
        children.append(Span(children=symbol[-1], className=class_name))
    return children
