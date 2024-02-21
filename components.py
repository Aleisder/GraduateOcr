from dash import dcc, html
from dash.dcc import Dropdown
from dash_mantine_components import Notification
from dash_iconify import DashIconify
from dash.html import Div, Img


def show_notification(title: str, message: str, icon: str):
    return Notification(
        id='notification',
        action='show',
        title=title,
        message=message,
        icon=DashIconify(icon=icon),
        styles={
            'body': {'width': '100%'},
            'title': {'fontSize': '36sp'}
        }
    )


FileUpload = dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Перетащите файл или ',
        html.A('Выберите его', style={'color': '#119DFF'})
    ]),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    },
    # Allow multiple files to be uploaded
    multiple=False
)

# FileUpload = Div(
#     className='flex-item',
#     children=dcc.Upload(
#         id='upload-data',
#         className='upload-component',
#         children=Div(
#             id='asgfhjgfjfgdfa',
#             className='icon-container',
#             children=Img(
#                 id='fhjhfg',
#                 src='./assets/images/icon_upload.svg',
#                 width=40,
#                 height=40,
#                 style={
#                     'color': 'white'
#                 }
#             )
#         ),
#         # Allow multiple files to be uploaded
#         multiple=False
#     )
# )

ChooseOcrDropDown = Div(
    id='test2',
    className='flex-item',
    children=Dropdown(
        id='dropdown-ocr-module',
        options=['EasyOCR', 'OpenCV'],
        value='EasyOCR',
        optionHeight=50,
        style={
            'width': '300px'
        }
    )
)
