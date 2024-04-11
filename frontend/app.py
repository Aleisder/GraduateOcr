import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Dash, callback, Output, Input, no_update, State, dcc
from dash.dcc import Loading
from dash.exceptions import PreventUpdate
from dash.html import Div, A
from dash_iconify import DashIconify
from pandas import DataFrame
from dash import html

import custom_dash_components as cdc
from api import OcrApi
from assessment import AssessmentService
from utils.character_analysis_rows_builder import build_from_dataframe
from utils.ui_helper import reference_text_span_formatted
from utils.colors import Color
from frontend.model import OcrDocument

app = Dash(
    name=__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

character_analysis_df: DataFrame = DataFrame([0])
assessment_service = AssessmentService()

api = OcrApi()

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
                    dmc.Group([
                        cdc.FileUpload('upload-data'),
                        dmc.ActionIcon(
                            id='delete-file-action-icon',
                            children=[DashIconify(icon='streamline:delete-1-solid')],
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
                        cdc.SelectLanguage('document-language-radio-group'),
                        dmc.Button(
                            id='recognize-button',
                            children='Начать распознание',
                            rightIcon=DashIconify(icon='material-symbols:search'),
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
                            dbc.Accordion([
                                dbc.AccordionItem(
                                    id='recognition-result-accordion-item',
                                    children=[
                                        dmc.Group([
                                            cdc.ColorMetrics(
                                                metrics=[
                                                    {'color': '#A2E0B2', 'metric': 'Символ распознан верно'},
                                                ]
                                            ),
                                            cdc.ColorMetrics(
                                                metrics=[
                                                    {'color': '#FFE65F', 'metric': 'Пропущенный символ'},
                                                ]
                                            ),
                                            cdc.ColorMetrics(
                                                metrics=[
                                                    {'color': '#FFBBAE', 'metric': 'Добавлен лишний символ'},
                                                ]
                                            )
                                        ]),
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

                                        ]),
                                        cdc.ColorMetrics(
                                            metrics=[
                                                {'color': '#FFE65F', 'metric': 'Добавленный символ'},
                                                {'color': '#FFBBAE', 'metric': 'Удаленный символ'}
                                            ]
                                        ),
                                        dmc.Table(
                                            id='recognition-result-table',
                                            highlightOnHover=True
                                        )
                                    ],
                                    title='Результаты распознания'
                                ),
                                dbc.AccordionItem(
                                    id='general-analysis-accordion-item',
                                    title='Общий анализ',
                                    children=[]
                                ),
                                dbc.AccordionItem(
                                    id='character-analysis-accordion-item',
                                    title='Символьный анализ (CER)',
                                    children=[
                                        cdc.CharacterAnalysisColorMetrics(),
                                        dmc.Group(
                                            align='top',
                                            children=[
                                                cdc.SymbolTypeRadioGroup('character-table-options-radio-group'),
                                                dmc.Divider(orientation='vertical', style={'margin': '8px'}),
                                                cdc.AccuracyRadioGroup('accuracy-table-options-radio-group')
                                            ]
                                        ),
                                        Div(
                                            style={
                                                'margin-top': '25px',
                                                'margin-bottom': '10px'
                                            },
                                            children=[
                                                dmc.Menu([
                                                    dmc.MenuTarget(dmc.Button('Скачать', variant='outline')),
                                                    dmc.MenuDropdown([
                                                        dmc.MenuLabel('Доступные форматы'),
                                                        dmc.MenuItem(
                                                            id='download-csv-menu-item',
                                                            children=[
                                                                dmc.Group([
                                                                    dmc.Image(
                                                                        src='assets/icons/csv-icon.png',
                                                                        width=25,
                                                                        height=25
                                                                    ),
                                                                    dmc.Text(
                                                                        children='.CSV',
                                                                        weight=500
                                                                    )
                                                                ]),
                                                                dcc.Download(id='download-csv')
                                                            ]
                                                        ),
                                                        dmc.MenuDivider(),
                                                        dmc.MenuItem(
                                                            id='download-xlsx-menu-item',
                                                            children=[
                                                                dmc.Group([
                                                                    dmc.Image(
                                                                        src='assets/icons/xlsx-icon.png',
                                                                        width=25,
                                                                        height=25
                                                                    ),
                                                                    dmc.Text(
                                                                        children='.XLSX',
                                                                        weight=500
                                                                    )
                                                                ]),
                                                                dcc.Download(id='download-xlsx')
                                                            ]
                                                        ),
                                                        dmc.MenuDivider(),
                                                        dmc.MenuItem(
                                                            id='download-json-menu-item',
                                                            children=[
                                                                dmc.Group([
                                                                    dmc.Image(
                                                                        src='assets/icons/json-icon.png',
                                                                        width=25,
                                                                        height=25
                                                                    ),
                                                                    dmc.Text(
                                                                        children='.JSON',
                                                                        weight=500
                                                                    )
                                                                ]),
                                                                dcc.Download(id='download-json')
                                                            ]
                                                        )
                                                    ]),
                                                ]),
                                            ]
                                        ),
                                        dmc.Table(
                                            id='character-analysis-table',
                                            className='accuracy-table',
                                            highlightOnHover=True
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
                    )
                ]
            )
        ]
    )
)


@callback(
    Output('upload-data', 'children', allow_duplicate=True),
    Output('upload-data', 'contents'),
    Input('delete-file-action-icon', 'n_clicks'),
    prevent_initial_call=True
)
def delete_file(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return Div([
        'Перетащите файл или ',
        A('Выберите', style={'color': '#119DFF'}),
    ]), None


@callback(
    Output('character-analysis-table', 'children', allow_duplicate=True),
    Input('character-table-options-radio-group', 'value'),
    prevent_initial_call=True
)
def change_symbol_type(value):
    df = assessment_service.filter_by_symbol_type(value)
    return build_from_dataframe(df)


@callback(
    Output('character-analysis-table', 'children', allow_duplicate=True),
    Input('accuracy-table-options-radio-group', 'value'),
    prevent_initial_call=True
)
def change_accuracy_option(value):
    df = assessment_service.last_df.copy()
    if value == 'any':
        return build_from_dataframe(df)
    elif value == '100':
        return build_from_dataframe(df.query('accuracy == 100'))
    elif value == '0':
        return build_from_dataframe(df.query('accuracy == 0'))


@callback(
    Output('download-csv', 'data'),
    Input('download-csv-menu-item', 'n_clicks'),
    prevent_initial_call=True
)
def download_table_csv(_):
    return dcc.send_data_frame(
        writer=assessment_service.current_df.to_csv,
        filename='character-analysis.csv'
    )


@callback(
    Output('download-xlsx', 'data'),
    Input('download-xlsx-menu-item', 'n_clicks'),
    prevent_initial_call=True
)
def download_table_xlsx(_):
    return dcc.send_data_frame(
        writer=assessment_service.current_df.to_excel,
        filename='character-analysis.xlsx',
        sheet_name='table-1'
    )


@callback(
    Output('download-json', 'data'),
    Input('download-json-menu-item', 'n_clicks'),
    prevent_initial_call=True
)
def download_json(_):
    return dcc.send_string(
        src=assessment_service.current_df.to_json,
        filename='character-analysis.json',
    )


def parse_contents(file: str, lang):
    if file is None:
        raise PreventUpdate
    _, content_string = file.split(',')
    return api.recognise(content_string)


@callback(
    Output('recognize-button', 'disabled'),
    Input('document-language-radio-group', 'value'),
    State('upload-data', 'contents')
)
def update_button_state(value, file):
    return value is None or file is None


@callback(
    Output('reference-text-div', 'children'),
    Output('experimental-text-div', 'children'),
    Output('notification-container', 'children'),
    Output('character-analysis-table', 'children'),
    Output('recognition-result-table', 'children'),
    Input('recognize-button', 'n_clicks'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('document-language-radio-group', 'value'),
    prevent_initial_call=True
)
def recognize_button_click(n_clicks, file, filename, lang):
    if any([n_clicks, file, filename]) is None:
        raise PreventUpdate
    if 'pdf' in filename:
        _, content_string = file.split(',')

        reference = api.reference_from_file(content_string)
        experimental = api.experimental_from_file(content_string)

        ocr_document = OcrDocument(reference, experimental)

        ref_text, exp_text = ocr_document.to_plain_text()

        char_analysis_df: DataFrame = assessment_service.character_analysis(ref_text, exp_text)
        table_rows = build_from_dataframe(char_analysis_df)

        reference_formatted = reference_text_span_formatted(reference)
        experimental_formatted = assessment_service.experimental_span_formatted(reference, experimental)

        recognition_rows = assessment_service.build_two_columns(reference, experimental)

        return reference_formatted, experimental_formatted, no_update, table_rows, recognition_rows
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
        port=5010
    )
