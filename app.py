import base64

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import Dash, dcc, callback, Output, Input, no_update, State
from dash.dcc import Loading
from dash.exceptions import PreventUpdate
from dash.html import Div
from dash_iconify import DashIconify
from pdf2image import convert_from_bytes

import custom_dash_components as cdc
from assessment import AssessmentService
from config import POPPLER_PATH
from ocr_modules.pytesseract_module import PytesseractModule
from ocr_service import OcrService

style = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

assessment_service = AssessmentService()

ocr_service = OcrService(
    reference=PytesseractModule(),
    experimental=PytesseractModule()
)

app.layout = dmc.NotificationsProvider(
    Div(
        id='main-container',
        className='main-container',
        children=[
            Div(id='notification-container'),
            Div(
                id='manage-container',
                className='border-container',
                children=[
                    dmc.Group(
                        [
                            cdc.FileUpload('upload-data'),
                            dmc.ActionIcon(
                                id='delete-file-action-icon',
                                children=[DashIconify(icon='streamline:delete-1-solid')]
                            ),
                            cdc.SelectOcrModule('ocr-modules-multi-select'),
                            cdc.SelectLanguage('document-language-radio-group'),
                            cdc.StartRecognitionButton('recognize-button')
                        ]
                    )
                ]
            ),
            Loading(
                id='loading-container',
                children=[
                    Div(
                        className='border-container',
                        children=[
                            dbc.Accordion([
                                dbc.AccordionItem(
                                    id='recognition-result-accordion-item',
                                    children=[
                                        dmc.Group([
                                            Div([
                                                dmc.Group(
                                                    position='apart',
                                                    children=[
                                                        dmc.Text('Эталонное решение'),
                                                        cdc.CopyClipboardButton(
                                                            component_id='test2',
                                                            read_from_component_id='reference-text-div'
                                                        )
                                                    ]
                                                ),
                                                cdc.TextContainer('reference-text-div')
                                            ]),
                                            Div([
                                                dmc.Text('Экспериментальное решение'),
                                                cdc.TextContainer('experimental-text-div')
                                            ])
                                        ])

                                    ],
                                    title='Результаты распознания'
                                ),
                                dbc.AccordionItem(
                                    id='general-analysis-accordion-item',
                                    title='Общий анализ',
                                    children=['Test']
                                ),
                                dbc.AccordionItem(
                                    id='character-analysis-accordion-item',
                                    title='Символьный анализ (CER)',
                                    children=[
                                        dmc.Paper(
                                            shadow='lg',
                                            radius='lg',
                                            m='15px',
                                            p='15px',
                                            children=[
                                                dmc.Grid([
                                                    Div(style={
                                                        'background': 'red',
                                                        'width': '20px',
                                                        'height': '20px',
                                                        'border-radius': '7px',
                                                        'margin': '10px'
                                                    }),
                                                    dmc.Text(' - все символы распознаны верно (100%)')
                                                ]),
                                                dmc.Grid([
                                                    Div(style={
                                                        'background': 'red',
                                                        'width': '20px',
                                                        'height': '20px',
                                                        'border-radius': '7px'
                                                    }),
                                                    dmc.Text(' - все символы распознаны верно (100%)')
                                                ])
                                            ]
                                        )
                                    ]
                                ),
                                dbc.AccordionItem(
                                    id='word-analysis-accordion-item',
                                    title='Словесный анализ (WER)',
                                    children=[]
                                ),
                                dbc.AccordionItem(
                                    id='page-analysis-accordion-item',
                                    children=['Content 3'],
                                    title='Анализ по страницам'
                                )
                            ])
                        ]
                    ),
                    dcc.Graph(id='cer-wer-histogram')
                ]
            )
        ]
    )
)


def parse_contents(file):
    if file is None:
        raise PreventUpdate
    content_type, content_string = file.split(',')
    decoded = base64.b64decode(content_string)

    images = convert_from_bytes(
        pdf_file=decoded,
        poppler_path=POPPLER_PATH
    )
    reference, experimental = '', ''

    for image in images:
        ref_page, exp_page = ocr_service.get_recognitions(image)
        reference += ref_page
        experimental += exp_page
    return reference, experimental


@callback(
    Output('recognize-button', 'disabled'),
    Input('document-language-radio-group', 'value'),
    State('upload-data', 'contents')
)
def update_button_state(value, file):
    if file is None:
        return True
    return value is None


@callback(
    Output('reference-text-div', 'children'),
    Output('experimental-text-div', 'children'),
    Output('notification-container', 'children'),
    Output('cer-wer-histogram', 'figure'),
    Output('character-analysis-accordion-item', 'children'),
    Input('recognize-button', 'n_clicks'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def recognize_button_click(n_clicks, file, filename):
    if any([n_clicks, file, filename]) is None:
        raise PreventUpdate
    if 'pdf' in filename:
        ref, exp = parse_contents(file)
        exp_formatted = assessment_service.build_from_differ_compare(ref, exp)
        char_analysis_df: pd.DataFrame = assessment_service.character_analysis(ref, exp)
        figure = {
            'data': [
                {'x': ['Словесное сравнение (WER)', ' Символьное CER'], 'y': [1, 1], 'type': 'bar', 'name': 'Эталон'},
                {'x': ['Словесное сравнение (WER)', ' Символьное CER'], 'y': [0.3, 0.3], 'type': 'bar',
                 'name': 'Экспериментальное'},
            ],
            'layout': {
                'title': 'Сравнение результатов распознавания'
            }
        }
        print(ref)

        return ref, exp_formatted, no_update, figure, cdc.CharacterAnalysisTable(
            component_id='character-analysis-table', df=char_analysis_df)
    return no_update, no_update, dmc.Notification(
        id='notification',
        action='show',
        title='Invalid file format',
        message='Only PDF files are allowed. Please, try again',
        icon=DashIconify(icon='material-symbols:error-outline'),
        styles={
            'body': {'width': '100%'},
            'title': {'fontSize': '36sp'}
        }
    ), no_update, no_update


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )
