import pandas
from dash import dcc, html, callback, Output, Input, State
from dash.development.base_component import _explicitize_args, Component
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import dash_mantine_components as dmc


def show_notification(title: str, message: str, icon: str):
    return dmc.Notification(
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


class CopyClipboardButton(dmc.ActionIcon):
    props = dict()

    def __init__(
            self,
            component_id: str,
            read_from_component_id: str
    ):
        self.props['id'] = component_id
        self.props['read_from'] = read_from_component_id

        super().__init__([
            dmc.ActionIcon(
                id=self.props['id'],
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

        @callback(
            Output(self.props['id'], 'display'),
            Input(self.props['id'], 'n_clicks'),
            State(self.props['read_from'], 'children'),
            prevent_initial_call=True
        )
        def copy_to_clipboard(n_clicks, text):
            if any([n_clicks, text]) is None:
                raise PreventUpdate
            pandas.DataFrame([text])[0][0].to_clipboard()
            return Component.UNDEFINED
