from dash import html, callback, Output, Input, State

import dash_mantine_components as dmc
from dash import dcc
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify


class FileUpload(dcc.Upload):
    props = dict()

    def __init__(self, component_id: str):
        self.props['id'] = component_id

        super().__init__([
            dcc.Upload(
                id=component_id,
                children=html.Div([
                    'Перетащите файл или ',
                    html.A('Выберите', style={'color': '#119DFF'}),
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
                multiple=False
            )
        ])

        @callback(
            Output(self.props['id'], 'children'),
            Input(self.props['id'], 'contents'),
            State(self.props['id'], 'filename'),
            allow_duplicate=True
        )
        def change_content(file, filename):
            if file is None:
                raise PreventUpdate
            return dmc.Group([
                DashIconify(icon='bi:check'),
                dmc.Text(filename)
            ])
