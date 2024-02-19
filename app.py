import base64

import dash
import pandas
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, callback, Output, Input, no_update
from dash.dcc import Loading
from dash.exceptions import PreventUpdate
from dash.html import Div, Br, H3, Button
from dash_bootstrap_components import Spinner
from dash_iconify import DashIconify
from dash_mantine_components import Textarea, NotificationsProvider, Notification, Group
from pdf2image import convert_from_bytes

from assessment import get_page_analytics
from components import FileUpload, ChooseOcrDropDown
from components import show_notification
from config import POPPLER_PATH
from ocr_modules.easyocr_module import EasyOcrModule
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
app = dash.Dash(__name__)
ocr_service = OcrService(
    reference=PytesseractModule(),
    experimental=EasyOcrModule()
)

app.layout = NotificationsProvider(
    Div(
        id='main-container',
        className='main-container',
        children=[
            Div(id='notification-container'),
            Spinner(id=LOADING_SPINNER),
            Div(
                id='panel-container',
                className=FLEX_CONTAINER,
                children=[
                    FileUpload,
                    ChooseOcrDropDown,
                    Div(
                        id='test3',
                        className=FLEX_ITEM,
                        children=Button(
                            id='analyze',
                            className=BUTTON_ASSESSMENT,
                            children='MAKE RECOGNITION'
                        )
                    )
                ]
            ),
            Br(),
            H3(id='page_amount', children='0'),
            Loading(
                id='loading-container',
                children=[
                    Div([
                        Group(
                            children=[
                                Textarea(
                                    id=REF_TEXTAREA,
                                    label='Reference',
                                    autosize=True,
                                    maxRows=20,
                                    size='xl',
                                ),
                                Textarea(
                                    id=EXP_TEXTAREA,
                                    label='Experimental',
                                    autosize=True,
                                    maxRows=20,
                                    size='xl',
                                )
                            ],
                            spacing=20,
                            align='center',
                            grow=True
                        ),
                        H3(
                            id='fgkljf',
                            children=''
                        )
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
                        figure={
                            'data': [
                                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montréal'},
                            ],
                            'layout': {
                                'title': 'Dash Data Visualization'
                            }
                        }
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
                    ),
                    dcc.Graph(
                        figure=go.Figure(data=go.Line(x=[1, 2, 3, 4], y=[0.76, 0.81, 0.91, 0.97]))
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
    cer_arr, wer_arr = [], []

    for image in images:
        ref_page, exp_page = ocr_service.get_recognitions(image)
        wer, cer = get_page_analytics(ref_page, exp_page)
        cer_arr.append(cer)
        wer_arr.append(wer)
        reference += ref_page
        exp_page += exp_page
    print(cer_arr)
    print(wer_arr)
    return reference, experimental


def invalid_format_error():
    return Notification(
        id='invalid_format_notification',
        title='Error',
        message='Only PDF files are allowed',
        action='show',
        icon=DashIconify(icon='ic:round-celebration')
    )


@callback(
    Output('reference-textarea', 'value'),
    Output('experimental-textarea', 'value'),
    Output('notification-container', 'children'),
    Input('upload-data', 'contents')
)
def update_output(file):
    if file is None:
        raise PreventUpdate
    if 'pdf' in file:
        ref, exp = parse_contents(file)
        return ref, exp, no_update
    return no_update, no_update, show_notification('Invalid file format',
                                                   'Only PDF files are allowed. Please, try again',
                                                   'material-symbols:error-outline')


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )
