from dash.html import Span, Br


def reference_text_span_formatted(reference: list[list[str]]) -> list[Span]:
    rows = []
    for page in reference:
        for line in page:
            rows.append(Span(line))
            rows.append(Br())
    return rows
