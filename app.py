import base64

import dash_mantine_components as dmc
import pandas
import plotly.express as px
from dash import Dash, dcc, callback, Output, Input, no_update, State
from dash.dcc import Loading
from dash.exceptions import PreventUpdate
from dash.html import Div
from dash_bootstrap_components import Spinner
from dash_iconify import DashIconify
from pdf2image import convert_from_bytes

import utils.colored_text_builder
from components import FileUpload, show_notification, CopyClipboardButton
from config import POPPLER_PATH
from ocr_modules.pytesseract_module import PytesseractModule
from ocr_service import OcrService

LOADING_SPINNER = 'loading-spinner'
REF_TEXTAREA = 'reference-textarea'
EXP_TEXTAREA = 'experimental-textarea'
FLEX_CONTAINER = 'flex-container'
FLEX_ITEM = 'flex-item'
BUTTON_ASSESSMENT = 'button-assessment'
DROPDOWN_OCR_MODULE = 'dropdown-ocr-module'

style = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__)

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
            Spinner(id=LOADING_SPINNER),
            Div(
                id='border-containera',
                className='border-container',
                children=[
                    dmc.Group(
                        [
                            FileUpload,
                            dmc.MultiSelect(
                                id='ocr-modules-multi-select',
                                label='Выберите OCR-инструменты',
                                data=[
                                    {'value': 'tesseract', 'label': 'Tesseract'},
                                    {'value': 'keras', 'label': 'Keras'},
                                    {'value': 'pyocr', 'label': 'PyOCR'},
                                ],
                                value=['tesseract']
                            ),
                            dmc.RadioGroup(
                                id='document-language-radio-group',
                                children=[
                                    dmc.Radio('English', 'EN'),
                                    dmc.Radio('Japanese', 'JPN'),
                                    dmc.Radio('Chinese', 'CHI')
                                ],
                                label='Выберите язык документа',
                                orientation='vertical'
                            ),
                            dmc.Button(
                                id='recognize-button',
                                children='Начать распознание',
                                rightIcon=DashIconify(icon='material-symbols:search')
                            )
                        ])
                ]
            ),
            Loading(
                id='loading-container',
                children=[
                    Div(
                        className='border-container',
                        children=[
                            dmc.Group(
                                children=[
                                    Div([
                                        dmc.Group(
                                            position='apart',
                                            children=[
                                                dmc.Text('Эталонное решение'),
                                                CopyClipboardButton(
                                                    id='copy-reference-action-button-test',
                                                ),
                                                dmc.ActionIcon(
                                                    id='copy-reference-action-button',
                                                    children=DashIconify(
                                                        icon='bi:copy',
                                                        height=18,
                                                        width=18
                                                    ),
                                                    size=24,
                                                    n_clicks=0,
                                                    radius=5
                                                )
                                            ]
                                        ),
                                        Div(
                                            id='reference-text-div',
                                            className='recognized-text-container'
                                        )
                                    ]),
                                    Div(
                                        children=[
                                            dmc.Text('Экспериментальное решение'),
                                            Div(
                                                id='experimental-text-div',
                                                className='recognized-text-container'
                                            )
                                        ]
                                    )
                                ],
                                spacing=20,
                                align='center',
                                grow=True
                            ),
                            dcc.Graph(
                                id='cer-wer-histogram',
                                # figure={
                                #     'data': [
                                #         {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                #         {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montréal'},
                                #     ],
                                #     'layout': {
                                #         'title': 'Dash Data Visualization'
                                #     }
                                # }
                            ),
                        ])

                ]
            ),
            Div(
                id='assessment-container',
                children=[
                    dcc.Graph(
                        id='sdfgsdfg',
                        figure=px.line(
                            data_frame=pandas.DataFrame(
                                {
                                    'Pages': [1, 2, 3, 4],
                                    'CER': [0.76, 0.81, 0.91, 0.97]
                                }
                            ),
                            x='Pages',
                            y='CER',
                        ),
                        responsive=False
                    ),
                    dcc.Graph(
                        figure=px.histogram(
                            data_frame=pandas.DataFrame({
                                'Pages': [1, 2, 3, 4],
                                'CER': [0.76, 0.81, 0.91, 0.97]}
                            ),
                            x='Pages',
                            y='CER',
                            nbins=1
                        )
                    )
                ]
            )

        ])
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


def invalid_format_error():
    return dmc.Notification(
        id='invalid_format_notification',
        title='Error',
        message='Only PDF files are allowed',
        action='show',
        icon=DashIconify(icon='ic:round-celebration')
    )


@callback(
    Output('upload-data', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
)
def change_upload_component_content(file, filename):
    if file is None:
        raise PreventUpdate
    return dmc.Group([
        DashIconify(icon='bi:check'),
        dmc.Text(filename)
    ])


@callback(
    Output('reference-text-div', 'children'),
    Output('experimental-text-div', 'children'),
    Output('notification-container', 'children', allow_duplicate=True),
    Output('cer-wer-histogram', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def update_output(file, filename):
    if file is None:
        raise PreventUpdate
    if 'pdf' in filename:
        ref, exp = parse_contents(file)
        exp_formatted = utils.colored_text_builder.build_from_differ_compare(ref, exp)
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

        return ref, exp_formatted, no_update, figure
    return no_update, no_update, show_notification('Invalid file format',
                                                   'Only PDF files are allowed. Please, try again',
                                                   'material-symbols:error-outline'), no_update


@callback(
    Output('notification-container', 'children', allow_duplicate=True),
    Input('copy-reference-action-button', 'n_clicks'),
    State('reference-text-div', 'children'),
    prevent_initial_call=True
)
def copy_to_clipboard(n_clicks, text):
    if any([n_clicks, text]) is None:
        raise PreventUpdate
    pandas.DataFrame([text]).to_clipboard()
    return None


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )
