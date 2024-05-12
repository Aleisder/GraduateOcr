import dash_mantine_components as dmc
from dash import html
from dash.html import Span, Br
from frontend.custom_dash_components.recognition_results.ocr_image_drawer import OcrPageDrawer
from dash import callback


def reference_text_span_formatted(reference: list[list[str]]) -> list[Span]:
    rows = []
    for page in reference:
        for line in page:
            rows.append(Span(line))
            rows.append(Br())
    return rows


def image_card_from_url(url: str, drawer_id: str) -> dmc.Card:
    return dmc.Card(
        withBorder=True,
        shadow="sm",
        radius="md",
        h=600,
        w=380,
        children=[
            OcrPageDrawer(url, drawer_id)
        ]
    )
