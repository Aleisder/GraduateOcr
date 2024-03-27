import dash_mantine_components as dmc
import pandas as pd
from dash import html


class CharacterAnalysisTable(dmc.Table):
    def __init__(self, component_id: str, df: pd.DataFrame):

        header = [
            html.Thead(
                html.Tr(
                    [
                        html.Th('Символ'),
                        html.Th('Найдено совпадений'),
                        html.Th('Всего в тексте'),
                        html.Th('Точность, %')
                    ]
                )
            )
        ]

        rows = []
        for _, row in df.iterrows():

            accuracy = row['accuracy']

            if accuracy == 100:
                color = '#59FF85'
            elif 100 > accuracy >= 90:
                color = '#A6FFBD'
            elif 90 > accuracy >= 70:
                color = '#FFFC66'
            else:
                color = '#FF6D45'

            accuracy_cell = html.Div(
                dmc.Text(
                    row['accuracy'],
                    style={
                        'text-align': 'center'
                    }
                ),
                style={
                    'background-color': color,
                    'border-radius': '7px',
                    'padding': '3px'
                }
            )

            char_cell = dmc.Kbd(
                row['char'],
                style={'font-size': '140%'}
            )

            rows.append(
                html.Tr(
                    [
                        html.Td(char_cell),
                        html.Td(row['found']),
                        html.Td(row['actually']),
                        html.Td(accuracy_cell)
                    ]
                )
            )

        body = [html.Tbody(rows)]

        super().__init__([
            dmc.Table(
                id=component_id,
                children=[],
                highlightOnHover=True,
                style={
                    'display': 'block',
                    'width': '100%',
                    'overflow-x': 'auto'
                }
            )
        ])
