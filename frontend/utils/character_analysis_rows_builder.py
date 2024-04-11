import pandas as pd
import dash_mantine_components as dmc
from dash.html import Thead, Tr, Th, Td, Tbody, Div


def build_from_dataframe(df: pd.DataFrame):

    column_names = ['Символ', 'Найдено в тексте', 'Фактически в тексте', 'Точность, %']

    header = [Thead(Tr([Th(name) for name in column_names]))]

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

        accuracy_cell = Div(
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
            Tr(
                [
                    Td(char_cell),
                    Td(row['found']),
                    Td(row['actually']),
                    Td(accuracy_cell)
                ]
            )
        )
    body = [Tbody(rows)]
    return header + body
