import base64

import dash_mantine_components as dmc
import pandas
import plotly.express as px
from dash import Dash, dcc, callback, Output, Input, no_update, State, html
from dash.dcc import Loading
from dash.exceptions import PreventUpdate
from dash.html import Div
from dash_bootstrap_components import Spinner
from dash_iconify import DashIconify
from pdf2image import convert_from_bytes

import custom_dash_components as cdc
import utils.colored_text_builder
from config import POPPLER_PATH
from ocr_modules.pytesseract_module import PytesseractModule
from ocr_service import OcrService

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
            Spinner(id='loading-spinner'),
            Div(
                id='border-containera',
                className='border-container',
                children=[
                    dmc.Group(
                        [
                            cdc.FileUpload(
                                component_id='upload-data'
                            ),
                            dmc.ActionIcon(
                                id='delete-file-action-icon',
                                children=[DashIconify(icon='streamline:delete-1-solid')]
                            ),
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
                                                cdc.CopyClipboardButton(
                                                    component_id='test2',
                                                    read_from_component_id='reference-text-div'
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
    ), no_update


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )
