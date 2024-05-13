import dash_mantine_components as dmc
from dash import dcc
from dash import html
from dash.html import Span, Br
from dash_iconify import DashIconify


def reference_text_span_formatted(reference: list[list[str]]) -> list[Span]:
    rows = []
    for page in reference:
        for line in page:
            rows.append(Span(line))
            rows.append(Br())
    return rows


def image_card_from_url(url: str, index: str) -> dmc.Card:
    return dmc.Card(
        withBorder=True,
        shadow="sm",
        radius="md",
        h=600,
        w=380,
        children=[
            html.Img(
                id={
                    'type': 'clickable_image',
                    'index': index
                },
                className='page-image-preview',
                src=url,
                height=500
            ),
            dmc.Drawer(
                id={
                    'type': 'page-drawer',
                    'index': index
                },
                padding=30,
                children=[

                    dmc.Group([
                        dmc.Switch(
                            id={
                                'type': 'show-borders-switch',
                                'index': index
                            },
                            style={
                                'margin-bottom': '10px'
                            },
                            label='Отобразить результаты распознавания',
                            size='md'
                        ),
                        dmc.ActionIcon(
                            id={
                                'type': 'download-image-action-icon',
                                'index': index
                            },
                            children=DashIconify(icon='material-symbols:download', width=20),
                            size="lg",
                            variant='outline',
                            mb=10,
                        )
                    ]),
                    html.Img(
                        id={
                            'type': 'page-drawer-image',
                            'index': index
                        },
                        src=url,
                        height=800,
                        style={
                            'border': '2px solid black'
                        }
                    ),
                    dcc.Download(
                        id={
                            'type': 'page-download',
                            'index': index
                        }
                    )
                ],
                size='35%',
                title=[dmc.Title('Просмотр страницы документа', order=2)]
            )
        ]
    )
