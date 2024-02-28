import pandas
from dash import dcc, html, callback, Output, Input, State
from dash.exceptions import PreventUpdate
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
        'width': '250px',
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


class CopyClipboardButton(ActionIcon):
    def __init__(self, component_id: str, read_from_component_id: str):
        self.id = component_id
        self.read_from_component_id = read_from_component_id
        super().__init__([
            ActionIcon(
                id=self.id,
                children=DashIconify(
                    icon='bi:copy',
                    height=18,
                    width=18
                ),
                size=24,
                n_clicks=0,
                radius=5
            )
        ])

    # @callback(
    #     Output(),
    #     Input(read_from_component_id, 'children')
    # )
    # def copy_to_clipboard(self, text):
    #     if any([n_clicks, text]) is None:
    #         raise PreventUpdate
    #     pandas.DataFrame([text])[0].to_clipboard()
    #     return None


