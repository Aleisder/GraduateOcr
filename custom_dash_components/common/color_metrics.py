import dash_mantine_components as dmc
from dash.html import Div


class ColorMetrics(dmc.Paper):
    def __init__(self, metrics: list):
        super().__init__([
            dmc.Paper(
                shadow='lg',
                radius='lg',
                m='15px',
                p='20px',
                children=[
                    dmc.Grid(
                        m='5px',
                        children=[
                            Div(
                                style={
                                    'background': value['color'],
                                    'width': '20px',
                                    'height': '20px',
                                    'border-radius': '7px'
                                }
                            ),
                            dmc.Text(
                                children=value['metric']
                            )
                        ]
                    ) for value in metrics
                ]
            )
        ])
