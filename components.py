from dash import dcc, html
from dash_iconify import DashIconify
from dash_mantine_components import Notification, ActionIcon


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