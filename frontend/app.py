import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Dash, callback, Output, Input, no_update, State, dcc, MATCH, html
from dash.dcc import Loading
from dash.exceptions import PreventUpdate
from dash.html import Div, A
from dash_iconify import DashIconify
from pandas import DataFrame

import custom_dash_components as cdc
from api import OcrApi
from assessment import AssessmentService
from frontend.model import OcrDocument
from utils.character_analysis_rows_builder import build_from_dataframe
from utils.ui_helper import reference_text_span_formatted, image_card_from_url

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
            # контейнер для отображения уведомлений
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
                            children='Начать распознавание',
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
                                    id='document-pages-accordion-item',
                                    title='Страницы документа',
                                    children=[dmc.Center(id='pages-container')]
                                ),
                                dbc.AccordionItem(
                                    id='recognition-result-accordion-item',
                                    children=[
                                        dmc.Tabs(
                                            color='#119DFF',
                                            orientation='horizontal',
                                            value='full_text',
                                            children=[
                                                dmc.TabsList([
                                                    dmc.Tab(
                                                        children=[
                                                            dmc.Group([
                                                                dmc.Avatar(DashIconify(icon="radix-icons:star"),
                                                                           color="blue", radius="xl"),
                                                                dmc.Text("Текст целиком")
                                                            ])
                                                        ],
                                                        value="full_text"
                                                    ),
                                                    dmc.Tab(
                                                        children=[
                                                            dmc.Group([
                                                                dmc.Avatar(DashIconify(icon="ph:columns"),
                                                                           color="blue", radius="xl"),
                                                                dmc.Text("Построчно")
                                                            ])
                                                        ],
                                                        value='by_line'
                                                    ),
                                                ]),
                                                dmc.TabsPanel(
                                                    value='full_text',
                                                    children=[
                                                        cdc.ColorMetrics(
                                                            metrics=[
                                                                {'color': '#A2E0B2',
                                                                 'metric': 'Символ распознан верно'},
                                                                {'color': '#FFE65F',
                                                                 'metric': 'Пропущенный символ'},
                                                                {'color': '#FFBBAE',
                                                                 'metric': 'Добавлен лишний символ'},
                                                            ]
                                                        ),
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
                                                    ]
                                                ),
                                                dmc.TabsPanel(
                                                    value='by_line',
                                                    children=[
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
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    title='Результаты распознавания'
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


@callback(
    Output('recognize-button', 'disabled'),
    Input('document-language-radio-group', 'value'),
    State('upload-data', 'contents')
)
def update_button_state(value, file):
    return value is None or file is None


invalid_file_format_notification = dmc.Notification(
    id='notification',
    action='show',
    title='Invalid file format',
    message='Only PDF files are allowed. Please, try again',
    icon=DashIconify(icon='material-symbols:error-outline'),
    styles={
        'body': {'width': '100%'},
        'title': {'fontSize': '36sp'}
    }
)


@callback(
    Output('reference-text-div', 'children'),
    Output('experimental-text-div', 'children'),
    Output('notification-container', 'children', allow_duplicate=True),
    Output('character-analysis-table', 'children'),
    Output('recognition-result-table', 'children'),
    Output('pages-container', 'children'),
    Input('recognize-button', 'n_clicks'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('document-language-radio-group', 'value'),
    prevent_initial_call=True
)
def recognize_button_click(n_clicks, file, filename, lang):
    if any([n_clicks, file, filename]) is None:
        raise PreventUpdate

    if 'pdf' not in filename:
        return no_update, no_update, invalid_file_format_notification, no_update, no_update, no_update

    _, content_string = file.split(',')

    reference = api.reference_from_file(content_string)
    experimental = api.experimental_from_file(content_string, lang)

    ocr_document = OcrDocument(reference, experimental)

    ref_text, exp_text = ocr_document.to_plain_text()

    char_analysis_df: DataFrame = assessment_service.character_analysis(ref_text, exp_text)
    table_rows = build_from_dataframe(char_analysis_df)

    reference_formatted = reference_text_span_formatted(reference)
    experimental_formatted = assessment_service.experimental_span_formatted(reference, experimental)

    recognition_rows = assessment_service.build_two_columns(reference, experimental)

    urls = api.get_images_by_document(content_string)

    images = dmc.Group([image_card_from_url(url, i) for (i, url) in enumerate(urls)])
    return reference_formatted, experimental_formatted, no_update, table_rows, recognition_rows, images


@callback(
    Output({'type': 'page-drawer-image', 'index': MATCH}, 'src', allow_duplicate=True),
    Output({'type': 'page-drawer', 'index': MATCH}, 'opened'),
    Input({'type': 'clickable_image', 'index': MATCH}, 'n_clicks'),
    State({'type': 'clickable_image', 'index': MATCH}, 'src'),
    prevent_initial_call='initial_duplicate'
)
def open_drawer(n_clicks, url):
    print(n_clicks)
    if n_clicks is None:
        raise PreventUpdate
    return url, True


@callback(
    Output({'type': 'page-drawer-image', 'index': MATCH}, 'src', allow_duplicate=True),
    Input({'type': 'show-borders-switch', 'index': MATCH}, 'checked'),
    State({'type': 'page-drawer-image', 'index': MATCH}, 'src'),
    prevent_initial_call='initial_duplicate'
)
def show_symbols_borders(checked: bool, url: str):
    if checked:
        return url[:-4] + '-bordered.png'
    return url[:-13] + '.png'


@callback(
    Output({'type': 'page-download', 'index': MATCH}, 'data'),
    Input({'type': 'download-image-action-icon', 'index': MATCH}, 'n_clicks'),
    State({'type': 'page-drawer-image', 'index': MATCH}, 'src')
)
def download_page(n_clicks, url):
    if n_clicks is None:
        raise PreventUpdate
    return dcc.send_file(url)


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5010
    )
